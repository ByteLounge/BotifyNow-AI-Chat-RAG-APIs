def extract_text_from_pdf(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
        if len(text) > 3000:  # chunk size to prevent huge embeddings
            break
    return text
