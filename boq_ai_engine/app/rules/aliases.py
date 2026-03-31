DISCIPLINE_KEYWORDS = {
    'electrical': ['electrical', 'el-', 'lighting', 'socket', 'power', 'intercom', 'internet', 'db/', 'earthing'],
    'hvac': ['hvac', 'fcu', 'fan coil', 'duct', 'air conditioning', 'condensing unit', 'exhaust fan', 'copper pipe'],
    'plumbing': ['plumbing', 'drainage', 'water supply', 'w.c', 'municipality', 'floor drain', 'hwr', 'cwr'],
    'structural': ['structural', 'foundation', 'slab', 'columns', 'axis', 'reinforcement', 'ground beams', 'tank'],
    'architectural': ['architectural', 'door schedule', 'window schedule', 'elevation', 'site plan', 'furniture plan', 'dimension plan'],
}

ITEM_PATTERNS = {
    'lighting': ['light', 'lighting', 'led'],
    'sockets': ['socket', 'outlet', 'power socket'],
    'fcu': ['fcu', 'fan coil'],
    'heavy_equipment': ['oven', 'pump', 'charger', 'heater', 'condensing unit', 'exhaust fan'],
    'plumbing_fixture': ['w.c', 'bath', 'wash', 'drain', 'water tank', 'cwr', 'hwr'],
    'structural_element': ['foundation', 'beam', 'column', 'slab', 'reinforcement', 'tank'],
    'architectural_element': ['door', 'window', 'elevation', 'stair', 'site plan'],
}

DRAWING_CODE_PATTERNS = {
    'electrical': r'EL-?\d+|ELECT\s*\d+',
    'hvac': r'HVAC-?\d+|AC-?\d+',
    'plumbing': r'PL-?\d+',
    'structural': r'ST-?\d+',
    'architectural': r'AR-?\d+',
}
