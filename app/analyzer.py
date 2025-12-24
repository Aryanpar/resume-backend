def analyze_resume(text: str):
    text_lower = text.lower()

    score = 50
    feedback = []

    # --- Keyword Quality Check ---
    keywords = {
        "project": "Add a project section with details & impact.",
        "internship": "Mention your internships clearly with achievements.",
        "experience": "Add real world experience (internships, projects or jobs).",
        "skills": "Include a clear technical skills section."
    }

    for word, message in keywords.items():
        if word in text_lower:
            score += 5
        else:
            feedback.append(message)

    # --- Word Count Check ---
    words = len(text.split())
    if words < 120:
        feedback.append("Resume content is too short. Try 1–2 pages.")
        score -= 10
    elif words > 700:
        feedback.append("Resume is too long. Keep it concise.")
        score -= 5

    # --- Objective / Summary ---
    if "objective" not in text_lower and "summary" not in text_lower:
        feedback.append("Add a short career summary at the top.")
        score -= 5

    # --- Education Section ---
    if "education" not in text_lower:
        feedback.append("Add an Education section.")

    # --- Contact Info ---
    if "@" not in text_lower:
        feedback.append("Add contact email.")

    # --- Normalize Score ---
    score = max(0, min(100, score))

    return score, feedback
