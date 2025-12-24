def analyze_resume(text: str):
    feedback = []
    score = 50

    keywords = ["project", "internship", "experience", "skills"]

    for word in keywords:
        if word in text.lower():
            score += 5
        else:
            feedback.append(f"Add more details about your {word}.")

    if len(text.split()) < 150:
        feedback.append("Resume content is too short.")
        score -= 10

    if "objective" not in text.lower():
        feedback.append("Consider adding a clear career objective.")

    score = max(0, min(score, 100))

    return score, feedback
