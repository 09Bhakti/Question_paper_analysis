import fitz
import pytesseract
from PIL import Image

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text()
            if not page_text or len(page_text.strip()) < 20:
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                page_text = pytesseract.image_to_string(img)
            text += f"\n--- Page {page_num} ---\n{page_text.strip()}\n"
    return text.strip()
