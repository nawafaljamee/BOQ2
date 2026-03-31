import math
import pandas as pd
from app.classifiers.column_detector import detect_description_column, detect_quantity_column, detect_unit_column
from app.classifiers.item_classifier import classify_item
from app.classifiers.discipline_classifier import detect_discipline


def _to_number(value, default=1.0):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return default
    try:
        num = float(value)
        return num if num > 0 else default
    except Exception:
        return default


def extract_schedule_items(df: pd.DataFrame, source_file: str, source_ref: str, discipline_hint: str = 'general') -> list[dict]:
    description_col = detect_description_column(df)
    quantity_col = detect_quantity_column(df)
    unit_col = detect_unit_column(df)

    if not description_col:
        return []

    items = []
    for idx, row in df.iterrows():
        description = str(row.get(description_col, '')).strip()
        if not description or description.lower() == 'nan':
            continue
        if description.lower() in {'description', 'panel description'}:
            continue
        discipline = discipline_hint if discipline_hint != 'general' else detect_discipline(description, source_file)
        category, confidence = classify_item(description, discipline)
        quantity = _to_number(row.get(quantity_col), default=1.0) if quantity_col else 1.0
        unit = str(row.get(unit_col, 'item')).strip() if unit_col else 'item'
        items.append({
            'source_file': source_file,
            'source_ref': f'{source_ref} row {idx + 1}',
            'discipline': discipline,
            'category': category,
            'description': description,
            'quantity': quantity,
            'unit': unit or 'item',
            'confidence': round(confidence, 2),
        })
    return items[:400]
