from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.config import TEMPLATES_DIR
from app.services.boq_service import analyze_project_files

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get('/')
async def home(request: Request):
    return templates.TemplateResponse(request, 'index.html', {'result': None})


@router.post('/analyze')
async def analyze(request: Request, files: list[UploadFile] = File(...)):
    uploaded = []
    for file in files:
        uploaded.append((file.filename, await file.read()))
    result = analyze_project_files(uploaded)
    return templates.TemplateResponse(request, 'index.html', {'result': result})


@router.post('/api/analyze')
async def analyze_api(files: list[UploadFile] = File(...)):
    uploaded = []
    for file in files:
        uploaded.append((file.filename, await file.read()))
    return JSONResponse(analyze_project_files(uploaded))
