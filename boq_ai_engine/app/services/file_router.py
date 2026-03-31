from app.readers.excel_reader import read_excel_file
from app.readers.csv_reader import read_csv_file
from app.readers.pdf_text_reader import read_pdf_text


def route_file(contents: bytes, filename: str) -> tuple[str, dict]:
    lower = (filename or '').lower()
    if lower.endswith('.csv'):
        return 'csv', read_csv_file(contents)
    if lower.endswith(('.xlsx', '.xls', '.xlsm', '.xlsb')):
        return 'excel', read_excel_file(contents, filename)
    if lower.endswith('.pdf'):
        return 'pdf', read_pdf_text(contents)
    raise ValueError(f'Unsupported file type: {filename}')
