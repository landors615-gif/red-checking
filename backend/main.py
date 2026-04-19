"""
Red Checking MVP - Backend API
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.api import router as api_router

app = FastAPI(
    title="Red Checking API",
    version="0.1.0",
    description="小红书账号/内容 AI 检测分析 API",
)

# CORS — credentials=True requires explicit origins (not "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://landors615-gif.github.io",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "red-checking-api"}
