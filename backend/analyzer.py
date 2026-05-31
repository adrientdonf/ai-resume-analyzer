import re
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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
    'very','including','using','via','across','per','within','about','such',
    'looking','required','expected','excellent','strong','senior','build',
    'comfortable','familiarity','knowledge','libraries','engineering',
    'communication','methodologies','scalable','machine','position','team',
    'role','work','years','experience','ability','skills','background',
    'join','plus','preferred','bonus','must','nice','have','will','able',
    'good','great','high','large','small','new','old','big','low','top',
    'hiring','platform','storage','deploy','deployment','development',
    'engineer','learning','model','models','pipelines','pipeline','data',
    'processing','api','service','services','system','systems','solution',
    'solutions','product','products','project','projects','implement',
    'manage','design','designs','maintain','support','develop',
    'working','seeking','responsible','responsibilities','opportunity'
}

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'ci/cd', 'cicd', text)
    text = re.sub(r'scikit-learn', 'scikitlearn', text)
    text = re.sub(r'node\.js', 'nodejs', text)
    text = re.sub(r'next\.js', 'nextjs', text)
    text = re.sub(r'vue\.js', 'vuejs', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text

def extract_keywords(text: str) -> set:
    text = normalize(text)
    words = text.split()
    return set(w for w in words if w not in STOP_WORDS and len(w) >= 3)

def match_resume(resume_text: str, job_text: str) -> dict:
    job_keywords = extract_keywords(job_text)
    resume_keywords = extract_keywords(resume_text)

    matched = job_keywords & resume_keywords
    missing = job_keywords - resume_keywords

    recall = len(matched) / len(job_keywords) if job_keywords else 0.0
    score = round(recall * 100, 1)

    missing_skills = sorted(missing, key=len, reverse=True)[:15]

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""You are a career coach reviewing a resume. Write directly to the candidate using "you" — no placeholders like [Candidate Name]. Be specific and concise.

Match score: {score}%
Keywords matched: {", ".join(sorted(matched)[:20])}
Missing from resume: {", ".join(missing_skills)}

Write a short, friendly, personalized skill-gap analysis with 3-5 specific actionable recommendations. Be concise."""
        }],
        max_tokens=500
    )

    return {
        "match_percent": score,
        "missing_skills": missing_skills,
        "matched_skills": sorted(matched, key=len, reverse=True)[:15],
        "recommendations": response.choices[0].message.content
    }
