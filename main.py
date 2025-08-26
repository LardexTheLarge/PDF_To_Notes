import pdf_reader

pdf_text = pdf_reader.extract_text_from_pdf("Resume of Gabriel Vasquez.pdf")
chunks = pdf_reader.chunk_text(pdf_text)

notes = []

for i, chunk in enumerate(chunks):
    print(f"--- Streaming Notes for chunk {i+1} ---")
    note = pdf_reader.summarize_chunk(chunk)
    notes.append(note)
    print(f"\n--- End of Chunk {i+1} ---\n")