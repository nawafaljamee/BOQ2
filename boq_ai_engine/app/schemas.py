from pydantic import BaseModel
from typing import List, Optional

class ExtractedItem(BaseModel):
    source_file: str
    source_ref: str
    discipline: str
    category: str
    description: str
    quantity: float = 1
    unit: str = 'item'
    confidence: float = 0.0

class FileSummary(BaseModel):
    filename: str
    filetype: str
    discipline: str
    pages_or_sheets: int
    extracted_rows: int
    notes: List[str] = []

class ProjectResult(BaseModel):
    project_name: Optional[str] = None
    files: List[FileSummary]
    items: List[ExtractedItem]
    drawing_index: List[dict]
    warnings: List[str]
