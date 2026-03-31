import re
from app.classifiers.item_classifier import classify_item
from app.utils import clean_text


def extract_pdf_clue_items(text: str, source_file: str, discipline: str) -> list[dict]:
    cleaned = clean_text(text).lower()
    candidates = []

    phrase_patterns = {
        'electrical': ['lighting', 'power sockets', 'ground floor lighting plan', 'load schedules', 'earthing'],
        'hvac': ['fcu', 'fan coil unit', 'hvac load schedules', 'exhaust fan', 'copper pipe'],
        'plumbing': ['water supply layout', 'drainage system layout', 'water tank', 'floor drain'],
        'architectural': ['door schedule', 'window schedule', 'site plan', 'elevation'],
        'structural': ['foundations', 'ground beams slab', 'reinforcement tables', 'tank details'],
    }

    for phrase in phrase_patterns.get(discipline, []):
        if phrase in cleaned:
            category, confidence = classify_item(phrase, discipline)
            candidates.append({
                'source_file': source_file,
                'source_ref': 'pdf text clue',
                'discipline': discipline,
                'category': category,
                'description': phrase.title(),
                'quantity': 1,
                'unit': 'clue',
                'confidence': round(min(0.75, confidence), 2),
            })

    seen = set()
    dedup = []
    for item in candidates:
        key = (item['discipline'], item['category'], item['description'])
        if key not in seen:
            seen.add(key)
            dedup.append(item)
    return dedup
