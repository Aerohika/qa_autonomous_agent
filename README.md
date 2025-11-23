project:
  name: "Autonomous QA Agent — Test Case & Selenium Script Generation"
  author: "Aastha"
  repository: "https://github.com/Aerohika/qa_autonomous_agent"
  description: >
    An intelligent QA agent that ingests project documentation and HTML to build a knowledge base,
    generate grounded test cases, and output runnable Selenium Python scripts.

overview:
  features:
    - Ingests support documents: product specs, UX guidelines, APIs
    - Ingests checkout.html structure
    - Builds a knowledge base using embeddings + text chunking
    - Generates documentation-grounded test cases using RAG
    - Converts test cases into runnable Selenium Python scripts
  components:
    backend: "Flask backend handling ingestion, RAG pipeline, script generation"
    frontend: "Streamlit UI for uploads, agent interaction, script display"
    scripts: "Auto-generated Selenium Python scripts"

project_structure:
  - path: "assets/"
    description: "checkout.html + support documents"
  - path: "backend/"
    description: "Flask backend (app.py)"
  - path: "frontend/"
    description: "Streamlit app (streamlit_app.py)"
  - path: "generated_scripts/"
    description: "Auto-generated Selenium scripts"
  - path: "requirements.txt"
    description: "Python dependencies"

support_documents:
  required:
    - "checkout.html"
    - "product_specs.md"
    - "ui_ux_guide.txt"
    - "api_endpoints.json (optional)"
  purpose: >
    These documents act as the authoritative knowledge base.
    All test-case reasoning is grounded strictly in these documents.

requirements:
  python_version: "Python 3.10+ (tested on Python 3.13)"
  dependencies: "pip install -r requirements.txt"
  browsers:
    chrome: "Latest version required"
  chromedriver:
    note: "Must match the installed Chrome version"
    download: "https://googlechromelabs.github.io/chrome-for-testing/#stable"

run_instructions:
  backend:
    command: "cd backend && python app.py"
  frontend:
    command: "cd frontend && streamlit run streamlit_app.py"
  workflow:
    - "Upload support documents"
    - "Upload checkout.html"
    - "Click 'Build Knowledge Base'"
    - "Ask the agent to generate test cases"
    - "Select a test case"
    - "Click 'Generate Selenium Script'"
    - "Run or download the generated script"

selenium_usage:
  run_script:
    - "python generated_scripts/<script_name>.py"
  serve_html:
    local_server_command: "python -m http.server 8000"
    url: "http://localhost:8000/checkout.html"
  config:
    page_url: "Use the above localhost URL in scripts"
    chromedriver_path: "CHROMEDRIVER_PATH = r'C:/path/to/chromedriver.exe'"

excluded_files:
  reason: "Avoid large binaries, secrets, and environment files"
  do_not_upload:
    - "chromedriver.exe"
    - "venv/"
    - "chroma_db/"
    - ".env"
    - "*.png screenshots"

demo_video_requirements:
  duration: "5–10 minutes"
  must_include:
    - "Uploading documents"
    - "Uploading checkout.html"
    - "Building the knowledge base"
    - "Generating test cases"
    - "Selecting a test case"
    - "Generating Selenium script"
    - "Running script in browser"

troubleshooting:
  issues:
    total_price_not_updating: "JS error — check browser console"
    selenium_click_failure: "Increase WebDriverWait timeout"
    chromedriver_mismatch: "Install matching ChromeDriver"
    browser_closes_instantly: "Remove --headless during debugging"
    frontend_not_connecting: "Start Flask backend first"

contact:
  support: "Open an Issue on GitHub repository"

acknowledgment:
  project_based_on: "Assignment: Development of an Autonomous QA Agent for Test Case & Script Generation"
