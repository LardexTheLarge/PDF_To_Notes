import pdf_reader

chunks = pdf_reader.extract_text_from_pdf("CO_CDL_23.pdf", page_numbers=range(5,15))

notes = []

for i, chunk in enumerate(chunks):
    print(f"\n\n--- Notes {i+1} ---\n\n")
    note = pdf_reader.summarize_chunk(chunk)
    notes.append(note)

with open("Notes/Intro_notes.md", "w", encoding="utf-8") as file:
    for i, note in enumerate(notes):
        file.write(f"\n--- Note {i+1} ---\n{note}")