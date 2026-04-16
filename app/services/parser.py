import pdfplumber  # type: ignore
import re


def extract_text_from_pdf(file_path: str) -> str:
    """Extract and clean text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {e}")

    # Clean up: collapse multiple blank lines, strip excess whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()


def truncate_text(text: str, max_chars: int = 3000) -> str:
    """Hard-truncate text to max_chars; tries to break at a sentence boundary."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_period = truncated.rfind('.')
    if last_period > max_chars * 0.8:
        return truncated[:last_period + 1]
    return truncated