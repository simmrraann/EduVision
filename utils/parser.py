from pdfminer.high_level import extract_text
import io

def extract_text_from_pdf(file):
    return extract_text(io.BytesIO(file.read()))