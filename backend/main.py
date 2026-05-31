from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.analyzer import match_resume, improve_resume
from backend.pdf_parser import extract_text_from_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.post("/analyze")
async def analyze(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    file_bytes = await resume.read()
    resume_text = extract_text_from_pdf(file_bytes)
    result = match_resume(resume_text, job_description)
    return result
@app.post("/improve")
async def improve(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    file_bytes = await resume.read()
    resume_text = extract_text_from_pdf(file_bytes)
    result = improve_resume(resume_text, job_description)
    return result