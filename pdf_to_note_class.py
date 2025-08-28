import fitz
from tkinter import *
import tkinter as tk
from tkinter import ttk
import json
import requests

class PdfToNoteApp(tk.Tk):
    def __init__(self):
        super().__init__()


    def extract_text_from_pdf(pdf_path, page_numbers=None):
        """Gets text from a pdf using select pages or the whole file.

        Args:
            pdf_path (_type_): Put the path to a pdf file.
            page_numbers (_type_, optional): Can you an array to select certain pages [1,5,8]. You can use the range method to do a group of pages range(1,5). Defaults to None to read the whole pdf.

        Returns:
            _type_: The selected text from the pdf.
        """
        doc = fitz.open(pdf_path)
        chunks = []

        if page_numbers is None:
            page_numbers = range(len(doc))

        for page_num in page_numbers:
            if 0 <= page_num < len(doc):
                page = doc[page_num]
                page_text = page.get_text()
                chunks.append(page_text)
            else:
                print(f"Warning: Page {page_num} is out of range.")
        return chunks

    def summarize_chunk(chunk):
        url="http://localhost:11434/api/generate"
        payload={
                "model": "gpt-oss:20b",
                "prompt": f"Write basic notes about the following text:\n\n{chunk}",
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





    # Code to start the model and save to a file
    chunks = extract_text_from_pdf("CO_CDL_23.pdf", page_numbers=range(5,15))

    notes = []

    for i, chunk in enumerate(chunks):
        print(f"\n\n--- Notes {i+1} ---\n\n")
        note = summarize_chunk(chunk)
        notes.append(note)

    with open("Notes/Intro_notes.md", "w", encoding="utf-8") as file:
        for i, note in enumerate(notes):
            file.write(f"\n--- Note {i+1} ---\n{note}")