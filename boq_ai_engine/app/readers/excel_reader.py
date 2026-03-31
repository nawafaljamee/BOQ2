from io import BytesIO
import pandas as pd
from app.classifiers.column_detector import normalize_columns, detect_description_column


HEADER_KEYWORDS = {'description', 'desc', 'panel description', 'qty', 'quantity', 'ct'}


def _prepare_sheet(df_raw: pd.DataFrame) -> pd.DataFrame:
    header_row_index = None
    search_limit = min(15, len(df_raw))

    for idx in range(search_limit):
        row_values = [str(v).strip().lower() for v in df_raw.iloc[idx].tolist() if str(v).strip() and str(v).lower() != 'nan']
        score = sum(1 for value in row_values if value in HEADER_KEYWORDS)
        if score >= 2 or ('description' in row_values and len(row_values) >= 4):
            header_row_index = idx
            break

    if header_row_index is not None:
        header = [str(v).strip() if str(v).strip() and str(v).lower() != 'nan' else f'column_{i}' for i, v in enumerate(df_raw.iloc[header_row_index].tolist())]
        body = df_raw.iloc[header_row_index + 1:].copy()
        body.columns = header
        return normalize_columns(body.reset_index(drop=True))

    if 0 in df_raw.index:
        header = [f'column_{i}' if str(v).lower() == 'nan' else str(v).strip() for i, v in enumerate(df_raw.iloc[0].tolist())]
        body = df_raw.iloc[1:].copy()
        body.columns = header
        return normalize_columns(body.reset_index(drop=True))

    return normalize_columns(df_raw)


def _score_sheet(df: pd.DataFrame) -> int:
    if df.empty:
        return -1
    df = normalize_columns(df)
    score = 0
    desc_col = detect_description_column(df)
    if desc_col:
        score += 10
    text = ' '.join(str(x).lower() for x in df.head(20).astype(str).fillna('').values.flatten())
    for keyword in ['lighting', 'socket', 'fcu', 'fan coil', 'drainage', 'water', 'door', 'window', 'foundation', 'slab', 'power']:
        if keyword in text:
            score += 2
    return score


def read_excel_file(contents: bytes, filename: str) -> dict:
    engine = 'xlrd' if filename.lower().endswith('.xls') else None
    excel = pd.ExcelFile(BytesIO(contents), engine=engine)
    sheets = []
    best_df = None
    best_name = None
    best_score = -1

    for sheet_name in excel.sheet_names:
        df_raw = excel.parse(sheet_name, header=None)
        df = _prepare_sheet(df_raw)
        score = _score_sheet(df)
        sheets.append({'sheet_name': sheet_name, 'rows': int(df.shape[0]), 'cols': int(df.shape[1]), 'score': score})
        if score > best_score:
            best_score = score
            best_df = df
            best_name = sheet_name

    if best_df is None:
        raise ValueError('No readable sheet found')

    return {
        'best_sheet_name': best_name,
        'best_df': best_df,
        'sheet_count': len(excel.sheet_names),
        'sheets': sheets,
    }
