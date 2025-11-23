# **Autonomous QA Agent — Test Case & Selenium Script Generation**

**Author:** Aastha

**Repository:** [https://github.com/Aerohika/qa_autonomous_agent](https://github.com/Aerohika/qa_autonomous_agent)

**Demo Video:** [https://drive.google.com/file/d/1q5Uyf8qWpLbAfef9aKJK-5Dtnh818d_y/view?usp=drivesdk](https://drive.google.com/file/d/1q5Uyf8qWpLbAfef9aKJK-5Dtnh818d_y/view?usp=drivesdk)

---

##  **Project Overview**

The **Autonomous QA Agent** is an AI-powered testing system that:

* Ingests documentation such as product specs, UI/UX guidelines, and API references
* Ingests `checkout.html` and extracts DOM structure
* Builds a knowledge base using **embeddings + chunking**
* Generates QA test cases using a **RAG pipeline**
* Converts selected test cases into **fully runnable Selenium Python scripts**

This automates what would normally take hours of manual QA effort.

---

##  **Architecture**

### **Backend — Flask**

* Handles file ingestion
* Generates embeddings
* Manages vector DB
* Runs the RAG pipeline
* Generates Selenium scripts

### **Frontend — Streamlit**

* Upload documents
* Build knowledge base
* Ask agent for test cases
* Preview & download generated scripts

### **Generated Scripts**

Contains automatically generated Selenium scripts based on selected test cases.

### **Assets**

Contains:

* `checkout.html`
* product specs
* UI/UX guide
* optional API files

---

##  **Project Structure**

```
qa_autonomous_agent/
│
├── assets/                 # HTML + support documents
├── backend/                # Flask backend (app.py)
├── frontend/               # Streamlit UI (streamlit_app.py)
├── generated_scripts/      # Auto-generated Selenium scripts
├── requirements.txt        # Dependencies
└── README.md               # This document
```

---

##  **Required Support Documents**

| File                            | Purpose                                 |
| ------------------------------- | --------------------------------------- |
| `checkout.html`                 | DOM understanding, form fields, UI flow |
| `product_specs.md`              | Functional requirement grounding        |
| `ui_ux_guide.txt`               | UI rules, error messages                |
| `api_endpoints.json` (optional) | For API-based validations               |

---

##  **Setup Instructions**

### **Python Version**

```
Python 3.10 – 3.13 (tested on 3.13)
```

### **Install Dependencies**

```
pip install -r requirements.txt
```

### **Chrome + ChromeDriver**

* Chrome must be up-to-date
* ChromeDriver must match Chrome version
* Download:
  [https://googlechromelabs.github.io/chrome-for-testing/#stable](https://googlechromelabs.github.io/chrome-for-testing/#stable)

Inside generated scripts, update:

```
CHROMEDRIVER_PATH = r"C:/path/to/chromedriver.exe"
```

---

## **Running the Project**

### **Start Backend**

```bash
cd backend
python app.py
```

### **Start Frontend**

```bash
cd frontend
streamlit run streamlit_app.py
```

### **Workflow**

1. Upload support documents
2. Upload `checkout.html`
3. Click **Build Knowledge Base**
4. Ask the agent: “Generate test cases”
5. Select a test case
6. Click **Generate Selenium Script**
7. Download or run the script

---

## **Running Selenium Scripts**

### **Option 1 — Direct Execution**

```bash
python generated_scripts/<script_name>.py
```

### **Option 2 — Serve HTML locally**

```bash
cd assets
python -m http.server 8000
```

Use this URL inside scripts:

```
http://localhost:8000/checkout.html
```

---

## **Troubleshooting**

| Issue                    | Cause               | Fix                            |
| ------------------------ | ------------------- | ------------------------------ |
| Total price not updating | JS error            | Check browser console          |
| Selenium click failing   | DOM not ready       | Increase WebDriverWait timeout |
| Browser closes instantly | Headless mode       | Remove `--headless`            |
| Streamlit not connecting | Backend not running | Start Flask first              |
| ChromeDriver mismatch    | Wrong version       | Install matching version       |

---

##  **Demo Video Uploaded**

* Around 8 minutes 
* It shows:
  
  ✓ Uploading documents
  
  ✓ Uploading HTML
  
  ✓ Building knowledge base
  
  ✓ Generating test cases
  
  ✓ Generating Selenium script
  
  ✓ Running the script live

---

## **Acknowledgment**

This project is based on the assignment:
**“Development of an Autonomous QA Agent for Test Case & Script Generation”**

---
