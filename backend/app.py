from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import re

app = Flask(__name__)
CORS(app)

skills = [
    "python", "java", "react", "sql",
    "machine learning", "flask",
    "html", "css", "javascript",
    "deep learning", "data analysis"
]

sections = ["education", "experience", "projects", "skills"]

action_verbs = ["developed", "built", "implemented", "designed", "created"]

def extract_text(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content
    except Exception as e:
        print("Error:", e)
    return text.lower()

def grammar_check(text):
    issues = []
    if "  " in text:
        issues.append("Extra spaces detected")
    if len(text.split()) < 50:
        issues.append("Resume content seems too short")
    return issues

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    text = extract_text(file)

    # Skills
    found = [s for s in skills if s in text]
    missing = [s for s in skills if s not in text]
    skill_score = int((len(found) / len(skills)) * 100)

    # Sections
    section_scores = {}
    for sec in sections:
        section_scores[sec] = 100 if sec in text else 0

    # Action verbs
    verbs_found = [v for v in action_verbs if v in text]
    if not verbs_found:
        verb_feedback = ["Use action verbs like developed, built, implemented"]
    else:
        verb_feedback = []

    # Grammar
    grammar_issues = grammar_check(text)

    # ATS Score (combined)
    ats_score = int(
        (skill_score * 0.5) +
        (sum(section_scores.values()) / len(section_scores) * 0.3) +
        (100 if verbs_found else 50) * 0.2
    )

    # Suggestions
    suggestions = []
    if "react" not in found:
        suggestions.append("Add React projects to strengthen frontend profile")
    if "sql" not in found:
        suggestions.append("Include SQL/database experience")
    if "machine learning" not in found:
        suggestions.append("Add ML projects for AI roles")

    return jsonify({
        "ats_score": ats_score,
        "found_skills": found,
        "missing_skills": missing,
        "skill_score": skill_score,
        "section_scores": section_scores,
        "suggestions": suggestions,
        "grammar_issues": grammar_issues,
        "verb_feedback": verb_feedback
    })

if __name__ == "__main__":
    app.run(debug=True)