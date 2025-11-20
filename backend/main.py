from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from io import BytesIO
import PyPDF2
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Extract text from PDF
def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# ------------------------------- NEW FEATURE -------------------------------
# Rule checking endpoint
# ---------------------------------------------------------------------------

@app.post("/check-rules")
async def check_rules(
    file: UploadFile = File(...),
    rule1: str = Form(...),
    rule2: str = Form(...),
    rule3: str = Form(...)
):

    pdf_bytes = await file.read()
    text = extract_text_from_pdf(pdf_bytes)

    rules = [rule1, rule2, rule3]

    model = genai.GenerativeModel("models/gemini-flash-latest")

    prompt = f"""
You are a rule-checking AI. The user will give you a PDF text and 3 rules.
You must check each rule independently and return results in ONLY THIS JSON FORMAT:

[
  {{
    "rule": "...",
    "status": "pass/fail",
    "evidence": "exact sentence from PDF",
    "reasoning": "short explanation",
    "confidence": 0-100
  }}
]

Strict rules:
- Output must be valid JSON.
- Confidence must be an integer.
- Evidence must be taken from the PDF text.

PDF TEXT:
{text}

RULES:
{rules}
"""

    response = model.generate_content(prompt)

    return {"results": response.text}
