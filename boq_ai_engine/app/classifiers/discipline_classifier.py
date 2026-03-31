from app.rules.aliases import DISCIPLINE_KEYWORDS


def detect_discipline(text: str, filename: str = '') -> str:
    haystack = f"{filename} {text}".lower()
    scores = {}
    for discipline, keywords in DISCIPLINE_KEYWORDS.items():
        scores[discipline] = sum(2 if kw in filename.lower() else 1 for kw in keywords if kw in haystack)

    best = max(scores, key=scores.get) if scores else 'general'
    return best if scores.get(best, 0) > 0 else 'general'
