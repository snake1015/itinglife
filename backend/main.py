from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routers import user, article, category, comment, message, upload, banner
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user.router, prefix="/api/users", tags=["用户"])
app.include_router(article.router, prefix="/api/articles", tags=["文章"])
app.include_router(category.router, prefix="/api/categories", tags=["分类"])
app.include_router(comment.router, prefix="/api/comments", tags=["评论"])
app.include_router(message.router, prefix="/api/messages", tags=["留言"])
app.include_router(upload.router, prefix="/api/upload", tags=["上传"])
app.include_router(banner.router, prefix="/api/banners", tags=["轮播图"])

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

@app.get("/health")
def health():
    return {"status": "ok"}

# TODO: 按模块引入路由 