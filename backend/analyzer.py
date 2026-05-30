import re
import ollama

STOP_WORDS = {
    'a','an','the','and','or','but','in','on','at','to','for','of','with','by',
    'from','as','is','was','are','were','be','been','being','have','has','had',
    'do','does','did','will','would','could','should','may','might','shall',
    'can','our','your','their','its','we','you','they','this','that','these',
    'those','any','all','each','every','both','few','more','most','other',
    'into','through','during','before','after','above','below','between',
    'out','off','over','under','again','then','once','here','there','where',
    'why','how','what','which','who','whom','not','no','nor','so','yet',
    'either','neither','whether','while','although','because','since',
    'unless','until','well','also','just','only','own','same','than','too',
    'very','including','using','via','across','per','within','about','such'
}

def extract_words(text: str) -> set[str]:
    words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9]{2,}\b', text.lower())
    return set(w for w in words if w not in STOP_WORDS and len(w) >= 5)

def match_resume(resume_text: str, job_text: str) -> dict:
    job_words = extract_words(job_text)
    resume_words = extract_words(resume_text)

    matched = job_words & resume_words
    missing = sorted(job_words - resume_words, key=len, reverse=True)[:20]

    score = round(len(matched) / min(len(job_words), len(resume_words)) * 100, 1) if job_words else 0.0

    prompt = f"""
You are a career coach. A candidate applied for a job and their resume was analyzed.

Match score: {score}%
Skills/keywords missing from their resume: {", ".join(missing)}

Write a short, friendly, personalized skill-gap analysis with 3-5 specific recommendations
to improve their resume for this role. Be concise and actionable.
"""
    response = ollama.chat(
        model="llama3.2:1b",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "match_percent": score,
        "missing_skills": missing,
        "recommendations": response["message"]["content"]
    }