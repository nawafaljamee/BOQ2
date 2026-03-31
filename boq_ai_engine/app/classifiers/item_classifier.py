from app.rules.aliases import ITEM_PATTERNS


def classify_item(description: str, discipline: str = 'general') -> tuple[str, float]:
    text = (description or '').lower()
    best_category = 'uncategorized'
    best_score = 0

    for category, patterns in ITEM_PATTERNS.items():
        score = sum(1 for pattern in patterns if pattern in text)
        if discipline == 'electrical' and category in {'lighting', 'sockets', 'heavy_equipment'}:
            score += 0.2
        if discipline == 'hvac' and category == 'fcu':
            score += 0.5
        if discipline == 'plumbing' and category == 'plumbing_fixture':
            score += 0.5
        if discipline == 'structural' and category == 'structural_element':
            score += 0.5
        if discipline == 'architectural' and category == 'architectural_element':
            score += 0.5
        if score > best_score:
            best_category = category
            best_score = score

    confidence = min(0.95, 0.35 + best_score * 0.2) if best_score else 0.2
    return best_category, confidence
