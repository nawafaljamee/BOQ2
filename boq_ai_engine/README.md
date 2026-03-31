# BOQ AI Engine

A FastAPI web app for testing project-pack ingestion for construction files. It accepts Excel schedules and discipline PDFs, detects discipline type, extracts drawing-index clues, converts schedule rows into normalized BOQ-like items, and shows an interactive review UI.

## Supported files
- `.xls`
- `.xlsx`
- `.xlsm`
- `.xlsb`
- `.csv`
- `.pdf`

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## What it does today
- Multi-file upload
- Discipline detection from filename and document text
- Excel sheet scoring and best-sheet selection
- BOQ-like item extraction from schedules
- PDF drawing index clue extraction
- Basic pricing engine for test/demo
- Clean review UI

## Suggested next steps
- Stronger table extraction from PDFs
- OCR fallback
- Export to Excel/CSV
- Human review workflow
- Project persistence database
