CATEGORY_PRICES = {
    'lighting': 120,
    'sockets': 150,
    'fcu': 500,
    'heavy_equipment': 700,
    'plumbing_fixture': 180,
    'structural_element': 950,
    'architectural_element': 250,
    'uncategorized': 0,
}


def price_items(items: list[dict]) -> tuple[list[dict], float]:
    priced = []
    total = 0.0
    for item in items:
        rate = CATEGORY_PRICES.get(item['category'], 0)
        line_total = rate * float(item.get('quantity', 1) or 1)
        total += line_total
        enriched = dict(item)
        enriched['rate'] = rate
        enriched['line_total'] = round(line_total, 2)
        priced.append(enriched)
    return priced, round(total, 2)
