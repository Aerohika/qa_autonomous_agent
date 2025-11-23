from flask import Flask, request, jsonify
import os
import logging
from io import BytesIO

from kb import KnowledgeBase, chunk_text
from llm_client import generate_test_cases, generate_selenium_script

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Single global KB for simplicity
kb = KnowledgeBase()
html_cache = {"source": ""}  # store checkout.html source

# Default checkout path (try common project-relative location)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CHECKOUT_PATH_UNIX = os.path.join(BASE_DIR, "assets", "checkout.html")
DEFAULT_CHECKOUT_PATH_WIN = os.path.join(BASE_DIR, "assets", "checkout.html")  # same here; client may use Windows path

def _load_default_html_if_exists():
    """
    If no HTML was uploaded by the user, but a checkout.html exists in assets/,
    load it into html_cache so downstream endpoints have content to use.
    """
    if html_cache.get("source"):
        return True
    # try the default path(s)
    for p in (DEFAULT_CHECKOUT_PATH_UNIX, DEFAULT_CHECKOUT_PATH_WIN):
        try:
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                    html_cache["source"] = fh.read()
                    logger.info("Loaded default checkout HTML from: %s", p)
                    return True
        except Exception as e:
            logger.exception("Error loading default checkout HTML from %s: %s", p, e)
    return False


@app.route("/build_kb", methods=["POST"])
def build_kb():
    """
    Expects:
    - 'files': multiple uploaded docs (md/txt/json/pdf etc.) – from Streamlit
    - 'html': single checkout.html file
    """
    try:
        kb.clear()
        docs_to_add = []
        idx = 0

        # Support documents
        files = request.files.getlist("files")
        for f in files:
            filename = f.filename
            try:
                content = f.read().decode("utf-8", errors="ignore")
            except Exception:
                # binary PDFs or other files might need different handling; read raw and skip decode errors
                try:
                    content = f.read().decode("utf-8", errors="ignore")
                except Exception:
                    content = ""
            for chunk in chunk_text(content):
                docs_to_add.append({
                    "id": f"{filename}_{idx}",
                    "text": chunk,
                    "metadata": {"source_document": filename}
                })
                idx += 1

        # HTML file upload (preferred)
        html_file = request.files.get("html")
        if html_file:
            html_source = html_file.read().decode("utf-8", errors="ignore")
            html_cache["source"] = html_source
            for chunk in chunk_text(html_source):
                docs_to_add.append({
                    "id": f"checkout.html_{idx}",
                    "text": chunk,
                    "metadata": {"source_document": "checkout.html"}
                })
                idx += 1
        else:
            # If no upload provided, try loading default local checkout.html (useful for local dev)
            _load_default_html_if_exists()
            # If we loaded default html, we've already placed it in html_cache, but we still need to add it to docs_to_add
            if html_cache.get("source"):
                for chunk in chunk_text(html_cache["source"]):
                    docs_to_add.append({
                        "id": f"checkout.html_{idx}",
                        "text": chunk,
                        "metadata": {"source_document": "checkout.html"}
                    })
                    idx += 1

        if docs_to_add:
            kb.add_documents(docs_to_add)
            return jsonify({"status": "ok", "message": "Knowledge base built", "num_chunks": len(docs_to_add)})
        else:
            return jsonify({"status": "error", "message": "No documents provided"}), 400

    except Exception as e:
        logger.exception("Error building KB: %s", e)
        return jsonify({"status": "error", "message": f"Failed to build KB: {e}"}), 500


@app.route("/generate_test_cases", methods=["POST"])
def api_generate_test_cases():
    try:
        data = request.json or {}
        user_query = data.get("query", "")
        if not user_query:
            return jsonify({"error": "query is required"}), 400

        # retrieve context from KB
        contexts = kb.query(user_query, top_k=6)
        combined_context = "\n\n".join([c["text"] + f"\n(Source: {c['metadata'].get('source_document')})"
                                        for c in contexts])

        # Call LLM within try/except to avoid raw 500 pages.
        try:
            tc_markdown = generate_test_cases(combined_context, user_query)
            return jsonify({"test_cases_markdown": tc_markdown})
        except Exception as llm_err:
            logger.exception("LLM error while generating test cases: %s", llm_err)
            return jsonify({"error": f"LLM error: {llm_err}"}), 500

    except Exception as e:
        logger.exception("Error in generate_test_cases endpoint: %s", e)
        return jsonify({"error": f"Internal server error: {e}"}), 500


@app.route("/generate_selenium_script", methods=["POST"])
def api_generate_selenium_script():
    try:
        data = request.json or {}
        test_case_text = data.get("test_case_text", "")
        if not test_case_text:
            return jsonify({"error": "test_case_text is required"}), 400

        # small retrieval: get broader context for this feature
        contexts = kb.query(test_case_text, top_k=6)
        combined_context = "\n\n".join([c["text"] + f"\n(Source: {c['metadata'].get('source_document')})"
                                        for c in contexts])

        # Ensure we have some HTML source (either uploaded or default)
        if not html_cache.get("source"):
            loaded = _load_default_html_if_exists()
            if not loaded:
                return jsonify({"error": "No HTML source in knowledge base. Upload checkout.html first."}), 400

        html_source = html_cache["source"]

        # Call LLM to generate selenium script; handle exceptions gracefully
        try:
            script = generate_selenium_script(combined_context, test_case_text, html_source)
            return jsonify({"selenium_script": script})
        except Exception as llm_err:
            logger.exception("LLM error while generating selenium script: %s", llm_err)
            return jsonify({"error": f"LLM error: {llm_err}"}), 500

    except Exception as e:
        logger.exception("Error in generate_selenium_script endpoint: %s", e)
        return jsonify({"error": f"Internal server error: {e}"}), 500


@app.route("/get_checkout_path", methods=["GET"])
def get_checkout_path():
    """
    Helpful endpoint for the frontend or developer to discover the local default checkout.html path
    that will be used if no file is uploaded.
    """
    return jsonify({
        "default_paths": {
            "project_assets_path": DEFAULT_CHECKOUT_PATH_UNIX,
            "note": "If your file is in a different location, upload it via the UI or edit DEFAULT_CHECKOUT_PATH in backend/app.py"
        }
    })


if __name__ == "__main__":
    # Run with debug=False by default; set FLASK_ENV=development if you want tracebacks in console
    app.run(host="0.0.0.0", port=8000, debug=False, use_reloader=False)
