from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import STATIC_DIR
from app.routes.upload import router as upload_router

app = FastAPI(title='BOQ AI Engine', version='1.0.0')
app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), name='static')
app.include_router(upload_router)
