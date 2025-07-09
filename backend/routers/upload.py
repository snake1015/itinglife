from fastapi import APIRouter, File, UploadFile, Request
from fastapi.responses import JSONResponse
import os
from uuid import uuid4
from fastapi import status

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post('')
async def upload_file(request: Request, file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[-1].lower()
    filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    # 分块写入，支持大文件
    with open(file_path, 'wb') as f:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)
    # 构造完整可访问URL
    base_url = str(request.base_url).rstrip('/')
    url = f"{base_url}/static/uploads/{filename}"
    return JSONResponse({"url": url}, status_code=status.HTTP_201_CREATED) 