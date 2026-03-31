from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
DATA = Path('/mnt/data')


def test_home_page_loads():
    response = client.get('/')
    assert response.status_code == 200
    assert 'BOQ AI Engine' in response.text


def test_api_analyze_sample_pack():
    sample_files = [
        ('files', ('ALQUDUS ELECT.pdf', (DATA / 'ALQUDUS ELECT.pdf').read_bytes(), 'application/pdf')),
        ('files', ('ALQUDUS HVAC.pdf', (DATA / 'ALQUDUS HVAC.pdf').read_bytes(), 'application/pdf')),
        ('files', ('ALQUDUS PLUMBING.pdf', (DATA / 'ALQUDUS PLUMBING.pdf').read_bytes(), 'application/pdf')),
        ('files', ('ALQUDUS ARCH.pdf', (DATA / 'ALQUDUS ARCH.pdf').read_bytes(), 'application/pdf')),
        ('files', ('ALQUDUS STR.pdf', (DATA / 'ALQUDUS STR.pdf').read_bytes(), 'application/pdf')),
        ('files', ('SCHADUALES.xls', (DATA / 'SCHADUALES.xls').read_bytes(), 'application/vnd.ms-excel')),
    ]
    response = client.post('/api/analyze', files=sample_files)
    assert response.status_code == 200
    payload = response.json()
    assert payload['item_count'] > 0
    disciplines = {row['discipline'] for row in payload['files']}
    assert 'electrical' in disciplines
    assert 'hvac' in disciplines
    assert 'plumbing' in disciplines
    assert payload['grand_total'] >= 0
