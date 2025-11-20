# PDF Rule Checker – README

## 📌 Overview
The **PDF Rule Checker** is a simple web application that allows users to:
1. Upload a PDF document (2–10 pages).
2. Enter three custom rules.
3. Automatically evaluate those rules using an LLM (Gemini model).

For each rule, the system returns:
- **PASS / FAIL**
- **Evidence sentence from PDF**
- **Short reasoning**
- **Confidence score (0–100)**

This satisfies the exact requirements of the assignment.

---

## 🏗️ Project Structure
```
niyamr-pdf-checker/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   └── venv/
│
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   └── ...
    ├── package.json
    └── vite.config.js
```

---

## ⚙️ Technologies Used
### **Backend**
- Python 3 (FastAPI)
- PyPDF2 (PDF text extraction)
- Google Gemini API
- python-dotenv
- Uvicorn

### **Frontend**
- React (Vite)
- Fetch API (to communicate with backend)
- Simple HTML/CSS UI

---

## 🚀 How to Run the Backend
### **1️⃣ Go to backend folder:**
```
cd backend
```

### **2️⃣ Activate virtual environment:**
```
venv\Scripts\activate
```

### **3️⃣ Install dependencies:**
```
pip install -r requirements.txt
```

### **4️⃣ Ensure `.env` file exists:**
```
GEMINI_API_KEY=YOUR_API_KEY_HERE
```

### **5️⃣ Start FastAPI server:**
```
uvicorn main:app --reload --port 8000
```

### ✔ Backend will run at:
**http://127.0.0.1:8000**

---

## 🌐 How to Run the Frontend
### **1️⃣ Open frontend folder:**
```
cd frontend
```

### **2️⃣ Install dependencies:**
```
npm install
```

### **3️⃣ Start the dev server:**
```
npm run dev
```

### ✔ Frontend will run at:
**http://localhost:5173**

---

## 📤 How to Use the App
1. Open the frontend.
2. Upload any PDF document.
3. Enter 3 rules (example: “Document must contain a date”).
4. Click **Check Document**.
5. Results table appears showing:
   - PASS/FAIL
   - Evidence
   - Reasoning
   - Confidence

---

## 🧠 How the Rule Checking Works (Backend Logic)
1. Extract PDF text using PyPDF2.
2. Create a structured prompt containing:
   - PDF text
   - All 3 rules
3. Send the prompt to Gemini.
4. Gemini returns structured JSON for each rule.
5. Backend returns this JSON to frontend.

Example output:
```json
[
  {
    "rule": "Document must mention a date.",
    "status": "pass",
    "evidence": "Found 'Published 2024' on Page 1",
    "reasoning": "A publication year is present.",
    "confidence": 92
  }
]
```

---

## 🧪 Sample Testing
### Sample rules:
- The document must contain my name.
- The document must mention at least one date.
- The document must have a purpose section.

### Sample result:
```
PASS – Evidence: "Published 2024"
PASS – Evidence: "Career Objective"
PASS – Evidence: "V S P VISHNU VARDHAN"
```

---

## 📄 Requirements File (Backend)
Make sure backend has a `requirements.txt` generated using:
```
pip freeze > requirements.txt
```

typical requirements include:
```
fastapi
uvicorn
PyPDF2
google-generativeai
python-dotenv
```

---

## 🛠️ Future Enhancements
- Better UI (cards, tabs, animations)
- Support for more rules (not just 3)
- Export results as PDF
- Add user authentication

---

## ✅ Conclusion
This project fully satisfies the assignment:
✔ PDF upload
✔ User-defined rules
✔ LLM-based rule checking
✔ PASS/FAIL evaluation
✔ Evidence + reasoning + confidence
✔ Complete frontend + backend integration

.
## 📸 Screenshot of Working UI

![App UI](screenshots/ui-demo.png)
---



