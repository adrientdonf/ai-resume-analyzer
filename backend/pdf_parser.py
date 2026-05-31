import pdfplumber
import re
import io

def clean_text(text: str) -> str:
    protected = {'TensorFlow':'TENSORFLOWTOKEN', 'PyTorch':'PYTORCHTOKEN',
                 'FastAPI':'FASTAPITOKEN', 'PostgreSQL':'POSTGRESQLTOKEN',
                 'MongoDB':'MONGODBTOKEN', 'JavaScript':'JAVASCRIPTTOKEN',
                 'TypeScript':'TYPESCRIPTTOKEN', 'GitHub':'GITHUBTOKEN',
                 'NumPy':'NUMPYTOKEN', 'SciKit':'SCKITTOKEN'}
    for term, token in protected.items():
        text = text.replace(term, token)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    for term, token in protected.items():
        text = text.replace(token, term)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_from_pdf(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    return clean_text(text)