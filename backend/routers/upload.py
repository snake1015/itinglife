from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import os
from uuid import uuid4

router = APIRouter()
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../static/uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('/')
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[-1]
    filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    url = f"/static/uploads/{filename}"
    return JSONResponse({"url": url}) 