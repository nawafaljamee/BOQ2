import re
from collections import Counter


def clean_text(value: str) -> str:
    return re.sub(r'\s+', ' ', (value or '').replace('\x00', ' ')).strip()


def top_counts(values, limit=6):
    counter = Counter(v for v in values if v)
    return counter.most_common(limit)
