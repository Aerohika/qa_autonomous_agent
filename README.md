
# **Autonomous QA Agent — Test Case & Selenium Script Generation**

**Author:** Aastha

**Repository:** [https://github.com/Aerohika/qa_autonomous_agent](https://github.com/Aerohika/qa_autonomous_agent)

**Demo Video:** [https://drive.google.com/file/d/1q5Uyf8qWpLbfAef9aKJK-5Dtnh818d_y/view?usp=drivesdk](https://drive.google.com/file/d/1q5Uyf8qWpLbfAef9aKJK-5Dtnh818d_y/view?usp=drivesdk)

---

## **Project Overview**

The **Autonomous QA Agent** is an AI-powered testing system that:

* Ingests project documentation such as product specs, UI/UX guidelines, and API references
* Ingests `checkout.html` and extracts DOM structure
* Builds a knowledge base using **embeddings + chunking**
* Generates QA test cases using a **RAG pipeline**
* Converts selected test cases into **fully runnable Selenium Python scripts**

This automates what would normally take hours of manual QA work.

---

## **Architecture**

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

Holds automatically generated Selenium Python scripts.

### **Assets**

Contains:

* `checkout.html`
* product specs
* UI/UX guide
* optional API files

---

## **Project Structure**

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

## **Required Support Documents**

| File                            | Purpose                                 |
| ------------------------------- | --------------------------------------- |
| `checkout.html`                 | DOM understanding, form fields, UI flow |
| `product_specs.md`              | Functional requirement grounding        |
| `ui_ux_guide.txt`               | UI rules, error messages                |
| `api_endpoints.json` (optional) | For API-based validations               |

---

## **Setup Instructions**

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

Use inside scripts:

```
http://localhost:8000/checkout.html
```

---

# 🔧 **Usage**

This section explains how to use the Autonomous QA Agent end-to-end — from uploading documents to executing generated Selenium scripts.

---

## **1️⃣ Start the System**

### Backend (Flask)

```bash
cd backend
python app.py
```

Runs on: **[http://localhost:5000](http://localhost:5000)**

### Frontend (Streamlit)

```bash
cd frontend
streamlit run streamlit_app.py
```

Runs on: **[http://localhost:8501](http://localhost:8501)**

---

## **2️⃣ Upload Documents**

Inside the Streamlit UI:

* `checkout.html`
* `product_specs.md`
* `ui_ux_guide.txt`
* `api_endpoints.json` *(optional)*

These form the **knowledge base**.

---

## **3️⃣ Build the Knowledge Base**

Click:

### **🟦 Build Knowledge Base**

The system:

* Splits documents into chunks
* Generates embeddings
* Stores them into a vector database
* Prepares for RAG test-case generation

---

## **4️⃣ Generate Test Cases**

Ask the agent:

```
Generate test cases for the checkout page
```

Or more specific:

```
Create test cases for discount code validation
```

The agent returns well-structured test cases (IDs, steps, expected results).

---

## **5️⃣ Select a Test Case**

Choose any generated test case from the dropdown.

Example:

```
TC_DISCOUNT_001
```

You will see:

* Steps
* Preconditions
* Expected results

---

## **6️⃣ Generate Selenium Script**

Click:

### **🟩 Generate Selenium Script**

The agent outputs a runnable Selenium script with:

* element locators
* waits
* assertions
* logging
* exception handling

Script is saved in:

```
generated_scripts/<testcase>.py
```

---

## **7️⃣ Run the Generated Script**

### Option A — run directly

```bash
python generated_scripts/<script_name>.py
```

### Option B — if page must be served

```bash
cd assets
python -m http.server 8000
```

Use:

```
http://localhost:8000/checkout.html
```

---

## **8️⃣ View Results**

The script prints:

* Step logs
* Status: Pass / Fail
* Assertion messages
* Screenshots on failure

Example:

```
Test Case TC_DISCOUNT_001 PASSED SUCCESSFULLY!
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

## **Demo Video Uploaded**

* Around 8 minutes
* Shows full pipeline:
  ✓ Upload documents
  ✓ Upload HTML
  ✓ Build knowledge base
  ✓ Generate test cases
  ✓ Generate Selenium script
  ✓ Run script live

---

## **Acknowledgment**

Based on the assignment:
**“Development of an Autonomous QA Agent for Test Case & Script Generation”**

