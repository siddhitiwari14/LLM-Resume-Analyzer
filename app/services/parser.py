import pdfplumber # type: ignore

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def truncate_text(text, max_chars=2000):  # reduce from 4000
    return text[:max_chars]