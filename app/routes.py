from fastapi import APIRouter, UploadFile, File
from pypdf import PdfReader       # <-- BETTER than PyPDF2
from .analyzer import analyze_resume

router = APIRouter()


@router.post("/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):

    print("📥 FILE RECEIVED:", file.filename)

    reader = PdfReader(file.file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        print("PAGE TEXT:", extracted[:80] if extracted else "NULL")
        if extracted:
            text += extracted

    print("TEXT LENGTH =", len(text))

    if len(text.strip()) == 0:
        print("⚠ TEXT EMPTY — FALLBACK RESPONSE")
        return {
            "score": 0,
            "feedback": [
                "We couldn't read any text from your resume.",
                "This sometimes happens with Word PDFs or scanned resumes.",
                "Please export as: File → Save As → PDF (Standard)"
            ]
        }

    score, feedback = analyze_resume(text)

    print("FINAL SCORE =", score)
    print("FEEDBACK =", feedback)

    return {
        "score": score,
        "feedback": feedback
    }
