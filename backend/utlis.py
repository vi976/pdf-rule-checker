import pdfplumber
import re
import json
from typing import List, Dict

# Optional OCR: requires pytesseract and Pillow installed and Tesseract executable available
try:
    import pytesseract
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False

SYSTEM_PROMPT = (
    "You are an assistant that evaluates whether a document satisfies a single rule. "
    "Always answer in strict JSON with the keys: rule, status (pass/fail), evidence, reasoning, confidence. "
    "Evidence should be a short quoted sentence and the page number, e.g. \"Found in page 2: 'Published 2024'\". "
    "Return confidence as a number between 0 and 100. Do not include extra commentary outside the JSON."
)

SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+')

def extract_text_per_page(pdf_path: str, use_ocr: bool=False) -> List[Dict]:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, p in enumerate(pdf.pages, start=1):
            text = p.extract_text() or ''
            text = '\n'.join([ln.strip() for ln in text.splitlines() if ln.strip()])
            if not text and use_ocr and OCR_AVAILABLE:
                try:
                    im = p.to_image(resolution=200).original
                    text = pytesseract.image_to_string(im)
                    text = '\n'.join([ln.strip() for ln in text.splitlines() if ln.strip()])
                except Exception:
                    text = ''
            pages.append({'page': i, 'text': text})
    return pages

def build_prompt_for_rule(pages: List[Dict], rule: str) -> str:
    parts = []
    for p in pages:
        parts.append(f"[PAGE {p['page']}]:\n{p['text']}")
    doc = '\n\n'.join(parts)

    prompt = (
        f"Document pages below.\n\n{doc}\n\n"
        f"Check the following rule EXACTLY: \"{rule}\"\n"
        "Output a single JSON object with keys: rule, status (pass or fail), evidence (exact sentence + page),"
        " reasoning (1-2 sentences), confidence (0-100). If you quote text as evidence, ensure it appears verbatim in the document."
    )
    return prompt

def parse_llm_response(text: str, rule: str) -> Dict:
    text = text.strip()
    try:
        start = text.index('{')
        end = text.rindex('}')
        obj_text = text[start:end+1]
        obj = json.loads(obj_text)
        obj.setdefault('rule', rule)
        obj.setdefault('status', 'fail')
        obj.setdefault('evidence', '')
        obj.setdefault('reasoning', '')
        obj.setdefault('confidence', 20)
        return obj
    except Exception:
        return {'rule': rule, 'status': 'fail', 'evidence': '', 'reasoning': text[:400], 'confidence': 5}

def find_snippet_in_pages(snippet: str, pages: List[Dict]):
    snippet = snippet.strip()
    for p in pages:
        if not p['text']:
            continue
        if snippet in p['text']:
            sentences = SENTENCE_SPLIT_RE.split(p['text'])
            for s in sentences:
                if snippet in s:
                    return p['page'], s.strip()
            return p['page'], snippet
    return None

def verify_and_score(parsed: Dict, pages: List[Dict]) -> Dict:
    evidence = parsed.get('evidence','')
    confidence = int(parsed.get('confidence', 20) or 20)
    status = parsed.get('status','fail')

    if evidence:
        m = re.search(r"'(.+)'", evidence)
        if m:
            snippet = m.group(1)
        else:
            snippet = re.sub(r"^.*?:\s*", '', evidence)
        found = find_snippet_in_pages(snippet, pages)
        if found:
            page, sentence = found
            if status.lower() == 'pass':
                confidence = min(100, max(confidence, 70))
            else:
                confidence = min(80, max(confidence, 40))
            parsed['evidence'] = f"Found in page {page}: '{sentence}'"
            parsed['confidence'] = confidence
            return parsed
        else:
            parsed['confidence'] = max(5, int(confidence*0.4))
            parsed['reasoning'] = (parsed.get('reasoning','') + ' (evidence not found verbatim in extracted text)').strip()
            return parsed
    else:
        keywords = re.findall(r"\w+", parsed.get('rule',''))
        keywords = [k for k in keywords if len(k) > 3]
        found_any = False
        for p in pages:
            if any(k.lower() in p['text'].lower() for k in keywords):
                found_any = True
                break
        if found_any:
            parsed['confidence'] = min(60, int(parsed.get('confidence',20) + 30))
            parsed['reasoning'] = parsed.get('reasoning','') + ' (heuristic keyword match found)'
        else:
            parsed['confidence'] = int(parsed.get('confidence',20))
        return parsed
