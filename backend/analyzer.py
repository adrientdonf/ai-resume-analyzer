from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ollama

def get_keywords(text: str, top_n: int = 30) -> list[str]:
    vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
    vectorizer.fit([text])
    return list(vectorizer.get_feature_names_out())

def match_resume(resume_text: str, job_text: str) -> dict:
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, job_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    match_percent = round(float(score) * 100, 1)

    resume_keywords = set(get_keywords(resume_text))
    job_keywords = set(get_keywords(job_text))
    missing_skills = list(job_keywords - resume_keywords)

    prompt = f"""
You are a career coach. A candidate applied for a job and their resume was analyzed.

Match score: {match_percent}%
Skills/keywords missing from their resume: {", ".join(missing_skills)}

Write a short, friendly, personalized skill-gap analysis with 3-5 specific recommendations
to improve their resume for this role. Be concise and actionable.
"""
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    recommendations = response["message"]["content"]

    return {
        "match_percent": match_percent,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }