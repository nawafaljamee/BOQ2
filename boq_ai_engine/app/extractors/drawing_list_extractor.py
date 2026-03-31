import re
from app.rules.aliases import DRAWING_CODE_PATTERNS
from app.utils import clean_text


def extract_drawing_index(text: str, discipline: str) -> list[dict]:
    cleaned = clean_text(text)
    lines = re.split(r'(?<=[A-Za-z0-9])\s(?=[A-Z]{2,}|[A-Z]{1,4}-\d+)', cleaned)
    pattern = DRAWING_CODE_PATTERNS.get(discipline)
    if not pattern:
        return []

    matches = []
    for raw in lines:
        if re.search(pattern, raw, flags=re.IGNORECASE):
            code_match = re.search(pattern, raw, flags=re.IGNORECASE)
            if not code_match:
                continue
            code = code_match.group(0)
            title = raw.replace(code, '').strip(' -:')
            if len(title) < 3:
                title = raw.strip()
            matches.append({'drawing_no': code.upper(), 'title': title[:140]})
    dedup = []
    seen = set()
    for item in matches:
        key = (item['drawing_no'], item['title'])
        if key not in seen:
            seen.add(key)
            dedup.append(item)
    return dedup[:40]
