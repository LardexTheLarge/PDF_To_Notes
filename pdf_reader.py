import fitz
import json
import requests

def extract_text_from_pdf(pdf_path, page_numbers=None):
    """Gets text from a pdf using select pages or the whole file.

    Args:
        pdf_path (_type_): Put the path to a pdf file.
        page_numbers (_type_, optional): Can you an array to select certain pages [1,5,8]. You can use the range method to do a group of pages range(1,5). Defaults to None to read the whole pdf.

    Returns:
        _type_: The selected text from the pdf.
    """
    doc = fitz.open(pdf_path)
    text = ""

    if page_numbers is None:
        page_numbers = range(len(doc))

    for page_num in page_numbers:
        if 0 <= page_num < len(doc):
            page = doc[page_num]
            text += page.get_text()
        else:
            print(f"Warning: Page {page_num} is out of range.")
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
            "prompt": f"Write simple notes about each major section in the following text:\n\n{chunk}",
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