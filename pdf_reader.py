import fitz
import requests

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, max_tokens=1000):
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = []

    for para in paragraphs:
        if len(current_chunk) + len(para) < max_tokens:
            current_chunk += para + "\n"
        else:
            chunks.append(current_chunk)
            current_chunk = para + "\n"
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def summarize_chunk(chunk):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gpt-oss:20b",
            "prompt": f"Summarize the following text into concise notes:\n\n{chunk}",
            "stream": False
        }
    )