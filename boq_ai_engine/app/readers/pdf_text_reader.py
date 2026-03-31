from io import BytesIO
from pypdf import PdfReader
from app.utils import clean_text


def read_pdf_text(contents: bytes, max_pages: int = 3) -> dict:
    reader = PdfReader(BytesIO(contents))
    pages = []
    all_text_parts = []
    page_count = len(reader.pages)
    for idx in range(page_count):
        if idx < max_pages:
            text = clean_text(reader.pages[idx].extract_text() or '')
            all_text_parts.append(text)
            pages.append({'page_number': idx + 1, 'text_preview': text[:300]})
        else:
            pages.append({'page_number': idx + 1, 'text_preview': ''})
    return {
        'page_count': page_count,
        'pages': pages,
        'text': '\n'.join(all_text_parts),
    }
