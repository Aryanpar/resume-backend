from fastapi import APIRouter, UploadFile, File
from PyPDF2 import PdfReader
from .analyzer import analyze_resume

router = APIRouter()

@router.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files allowed"}

    reader = PdfReader(file.file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    if len(text.strip()) == 0:
        return {"error": "Could not extract text from PDF"}

    score, feedback = analyze_resume(text)

    return {
        "score": score,
        "feedback": feedback
    }
