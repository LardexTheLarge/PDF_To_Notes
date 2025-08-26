import fitz
import json
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
    url="http://localhost:11434/api/generate"
    payload={
            "model": "gpt-oss:20b",
            "prompt": f"Write detailed notes about each numbered section in the following text:\n\n{chunk}",
            "stream": True
    }

    response_text = ""

    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    token = data.get("response", "")
                    print(token, end="", flush=True)
                    response_text += token
                except json.JSONDecoderError:
                    print("\n[Stream chunk decode error]")

    return response_text