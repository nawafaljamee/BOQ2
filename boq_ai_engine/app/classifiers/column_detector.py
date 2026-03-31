import pandas as pd


DESCRIPTION_ALIASES = [
    'description', 'desc', 'item description', 'load description', 'panel description',
    'work description', 'material description', 'remarks', 'scope',
]
QUANTITY_ALIASES = ['qty', 'quantity', 'count', 'no', 'nos', 'unit count', 'ct']
UNIT_ALIASES = ['unit', 'uom']


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df


def detect_column(df: pd.DataFrame, aliases: list[str]) -> str | None:
    original_columns = list(df.columns)
    normalized_map = {str(col).strip().lower(): col for col in original_columns}
    for alias in aliases:
        if alias in normalized_map:
            return normalized_map[alias]

    for col in original_columns:
        cleaned = str(col).strip().lower()
        if any(alias in cleaned for alias in aliases):
            return col
    return None


def detect_description_column(df: pd.DataFrame) -> str | None:
    return detect_column(df, DESCRIPTION_ALIASES)


def detect_quantity_column(df: pd.DataFrame) -> str | None:
    return detect_column(df, QUANTITY_ALIASES)


def detect_unit_column(df: pd.DataFrame) -> str | None:
    return detect_column(df, UNIT_ALIASES)
