from collections import defaultdict, Counter
from app.classifiers.discipline_classifier import detect_discipline
from app.extractors.drawing_list_extractor import extract_drawing_index
from app.extractors.schedule_extractor import extract_schedule_items
from app.extractors.pdf_discipline_extractors import extract_pdf_clue_items
from app.services.file_router import route_file
from app.services.pricing_service import price_items


def analyze_project_files(uploaded_files: list[tuple[str, bytes]]) -> dict:
    file_summaries = []
    items = []
    drawing_index = []
    warnings = []
    project_name = None

    for filename, contents in uploaded_files:
        filetype, payload = route_file(contents, filename)

        if filetype in {'excel', 'csv'}:
            df = payload['best_df']
            sample_text = ' '.join(df.columns.astype(str)) + ' ' + ' '.join(df.head(12).astype(str).fillna('').values.flatten())
            discipline = detect_discipline(sample_text, filename)
            extracted = extract_schedule_items(df, filename, payload['best_sheet_name'], discipline)
            items.extend(extracted)
            file_summaries.append({
                'filename': filename,
                'filetype': filetype,
                'discipline': discipline,
                'pages_or_sheets': payload['sheet_count'],
                'extracted_rows': len(extracted),
                'notes': [f"Best sheet: {payload['best_sheet_name']}"]
            })
            if df.shape[0] and df.shape[1]:
                first_row = ' '.join(df.head(2).astype(str).fillna('').values.flatten())
                if not project_name and len(first_row) > 10:
                    project_name = first_row[:120]
        elif filetype == 'pdf':
            text = payload['text']
            discipline = detect_discipline(text, filename)
            extracted_index = extract_drawing_index(text, discipline)
            drawing_index.extend([{**x, 'source_file': filename, 'discipline': discipline} for x in extracted_index])
            clue_items = extract_pdf_clue_items(text, filename, discipline)
            items.extend(clue_items)
            file_summaries.append({
                'filename': filename,
                'filetype': filetype,
                'discipline': discipline,
                'pages_or_sheets': payload['page_count'],
                'extracted_rows': len(clue_items),
                'notes': [f"Drawing index matches: {len(extracted_index)}"]
            })
            if not project_name and text:
                project_name = text[:120]
        else:
            warnings.append(f'Unsupported file: {filename}')

    priced_items, grand_total = price_items(items)

    discipline_totals = defaultdict(float)
    category_totals = defaultdict(float)
    for item in priced_items:
        discipline_totals[item['discipline']] += item['line_total']
        category_totals[item['category']] += item['line_total']

    return {
        'project_name': project_name or 'Uploaded Project Pack',
        'files': file_summaries,
        'items': priced_items,
        'drawing_index': drawing_index,
        'warnings': warnings,
        'grand_total': grand_total,
        'discipline_totals': dict(sorted(discipline_totals.items())),
        'category_totals': dict(sorted(category_totals.items())),
        'item_count': len(priced_items),
    }
