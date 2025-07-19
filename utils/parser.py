import PyPDF2
import io

def extract_text_from_pdf(file):
    """Extract text from PDF file using PyPDF2"""
    try:
        # Reset file pointer to beginning
        file.seek(0)
        
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"