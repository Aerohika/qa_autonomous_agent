project:
  name: "Autonomous QA Agent — Test Case & Selenium Script Generation"
  author: "Aastha"
  repository: "https://github.com/Aerohika/qa_autonomous_agent"
  demo_video: "https://drive.google.com/file/d/1q5Uyf8qWpLbfAef9aKJK-5Dtnh818d_y/view?usp=drivesdk"
  description: >
    An intelligent autonomous QA agent that ingests project documentation and HTML structure,
    builds a knowledge base using embeddings, generates grounded test cases using RAG,
    and outputs fully runnable Selenium Python scripts.

overview:
  problem_statement: >
    Manual test case writing and Selenium scripting are time-consuming and error-prone.
    This project automates the entire pipeline—from documentation ingestion to executable scripts.
  features:
    - Ingests support documents: product specs, UX guidelines, API references
    - Ingests checkout.html structure and extracts DOM features
    - Builds a semantic knowledge base using embeddings + chunking
    - Uses RAG to generate documentation-grounded test cases
    - Converts selected test cases into runnable Selenium Python scripts
    - Streamlit UI for user interaction and script preview
    - Flask backend to manage ingestion, RAG pipeline, and script generation

architecture:
  components:
    backend:
      description: "Flask backend powering ingestion, vector DB, and RAG pipeline"
      location: "backend/app.py"
    frontend:
      description: "Streamlit-based UI for uploads, knowledge building, and script generation"
      location: "frontend/streamlit_app.py"
    generated_scripts:
      description: "Folder where final Selenium Python scripts are stored"
      location: "generated_scripts/"
    assets:
      description: "Support documents used for grounding (checkout.html, UI/UX guide, API, specs)"
      location: "assets/"

project_structure:
  - path: "assets/"
    description: "HTML + support documents"
  - path: "backend/"
    description: "Flask backend"
  - path: "frontend/"
    description: "Streamlit frontend"
  - path: "generated_scripts/"
    description: "Auto-generated Selenium scripts"
  - path: "requirements.txt"
    description: "Python dependencies"

support_documents:
  required:
    - checkout.html
    - product_specs.md
    - ui_ux_guide.txt
    - api_endpoints.json (optional)
  purpose: >
    These documents form the authoritative knowledge base.
    All test-case reasoning and script generation are strictly grounded in them.

setup:
  python_version: "Python 3.10 — 3.13 (tested on 3.13)"
  environment_setup:
    - "pip install -r requirements.txt"
    - "Ensure Chrome browser is updated"
  chromedriver:
    note: "Version must match installed Chrome"
    download: "https://googlechromelabs.github.io/chrome-for-testing/#stable"
    path_instruction: >
      Update CHROMEDRIVER_PATH inside generated scripts if needed.

run_instructions:
  start_backend:
    command: |
      cd backend
      python app.py
    note: "Runs on http://localhost:5000/"
  start_frontend:
    command: |
      cd frontend
      streamlit run streamlit_app.py
    note: "Runs on http://localhost:8501/"
  workflow:
    - "Upload support documents (specifications, UI/UX, API docs)"
    - "Upload checkout.html"
    - "Click 'Build Knowledge Base'"
    - "Request: 'Generate test cases'"
    - "Select a test case"
    - "Click 'Generate Selenium Script'"
    - "Download or run the script"

selenium_usage:
  run_script:
    command: "python generated_scripts/<script_name>.py"
  serve_html:
    local_server:
      command: "python -m http.server 8000"
      url: "http://localhost:8000/checkout.html"
    configuration:
      page_url_note: "Use the localhost URL in generated Selenium scripts"
      chromedriver_note: "Update CHROMEDRIVER_PATH if needed"

examples:
  test_case_generation: >
    User uploads checkout.html, product specs, and UX guidelines.
    The agent identifies form fields, cart logic, discount flow, errors, and expected behaviors.
    It generates test cases like TC_DISCOUNT_001 with steps, expected results, and validations.
  selenium_script_output: >
    Agent produces a full runnable Selenium Python script with waits, assertions, and UI interactions.

troubleshooting:
  total_price_not_updating: "Check JavaScript console for errors"
  selenium_click_failure: "Increase WebDriverWait timeout"
  chromedriver_mismatch: "Install the correct matching ChromeDriver"
  ui_not_loading: "Start the Flask backend before Streamlit frontend"
  browser_closes_immediately: "Remove --headless mode during debugging"

excluded_files:
  reason: "To Avoid unnecessary binaries and sensitive files in repository"
  do_not_upload:
    - chromedriver.exe
    - venv/
    - .env
    - chroma_db/
    - *.png
    - __pycache__/

demo_video_uploaded:
  duration: "around 8 minutes"
  It includes:
    - "Uploading support documents"
    - "Uploading checkout.html"
    - "Building knowledge base"
    - "Generating test cases"
    - "Selecting a test case"
    - "Generating Selenium script"
    - "Running the generated script live"

contact:
  support: "Open an Issue on the GitHub repository"

acknowledgment:
  based_on: "Assignment: Development of an Autonomous QA Agent for Test Case & Script Generation"
