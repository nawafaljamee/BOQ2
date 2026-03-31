from io import BytesIO
import pandas as pd
from app.classifiers.column_detector import normalize_columns


def read_csv_file(contents: bytes) -> dict:
    df = pd.read_csv(BytesIO(contents))
    df = normalize_columns(df)
    return {
        'best_sheet_name': 'csv',
        'best_df': df,
        'sheet_count': 1,
        'sheets': [{'sheet_name': 'csv', 'rows': int(df.shape[0]), 'cols': int(df.shape[1]), 'score': 1}],
    }
