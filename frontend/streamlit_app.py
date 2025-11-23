import streamlit as st
import requests
import json

BACKEND_URL = "http://127.0.0.1:8000"


def main():
    st.title("Autonomous QA Agent for Test Case & Script Generation")

    st.sidebar.header("Steps")
    st.sidebar.markdown("""
    1. Upload documents + checkout.html  
    2. Build knowledge base  
    3. Ask for test cases  
    4. Select a test case  
    5. Generate Selenium script  
    """)

    st.header("1. Upload Project Artifacts")
    support_files = st.file_uploader("Upload support documents (md, txt, json, etc.)",
                                     type=["md", "txt", "json", "pdf", "html"],
                                     accept_multiple_files=True)
    html_file = st.file_uploader("Upload checkout.html", type=["html"])

    if st.button("Build Knowledge Base"):
        if not support_files and not html_file:
            st.error("Please upload at least one document or HTML file.")
        else:
            files = []
            for f in support_files:
                files.append(("files", (f.name, f.getvalue(), "text/plain")))
            if html_file:
                files.append(("html", (html_file.name, html_file.getvalue(), "text/html")))

            with st.spinner("Building knowledge base..."):
                resp = requests.post(f"{BACKEND_URL}/build_kb", files=files)
            if resp.status_code == 200:
                st.success(f"KB built successfully! Details: {resp.json()}")
            else:
                st.error(f"Error building KB: {resp.text}")

    st.header("2. Generate Test Cases")
    query = st.text_area("Enter a feature/query for test cases:",
                         value="Generate all positive and negative test cases for the discount code feature.")
    if st.button("Generate Test Cases"):
        if not query.strip():
            st.error("Please enter a query.")
        else:
            with st.spinner("Generating test cases using Gemini..."):
                resp = requests.post(f"{BACKEND_URL}/generate_test_cases",
                                     json={"query": query})
            if resp.status_code == 200:
                data = resp.json()
                tc_md = data["test_cases_markdown"]
                st.markdown("### Generated Test Cases")
                st.markdown(tc_md)
                st.session_state["last_test_cases_markdown"] = tc_md
            else:
                st.error(f"Error: {resp.text}")

    st.header("3. Select Test Case & Generate Selenium Script")
    st.markdown("Copy-paste one full test case (row from table) below:")

    test_case_text = st.text_area("Test case to automate:")
    if st.button("Generate Selenium Script"):
        if not test_case_text.strip():
            st.error("Please paste a test case description.")
        else:
            with st.spinner("Generating Selenium script..."):
                resp = requests.post(f"{BACKEND_URL}/generate_selenium_script",
                                     json={"test_case_text": test_case_text})
            if resp.status_code == 200:
                data = resp.json()
                script = data["selenium_script"]
                st.markdown("### Selenium Python Script")
                st.code(script, language="python")
            else:
                st.error(f"Error: {resp.text}")


if __name__ == "__main__":
    main()
