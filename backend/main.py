
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
import os

from core.config import settings
from core.logger import setup_logging
from api.routes import router as api_router

app = FastAPI(title="Cate Agency Explorer")

# Setup logging
setup_logging()

# Add CORS middleware (optional, in case frontend needs it during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Be cautious with wildcard in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Serve static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Health check route
@app.get("/health")
def health():
    return {
        "status": {
            "is_good": True,
            "message": "healthy",
            "debug": False,
            "env": settings.ENVIRONMENT,
            "duration": "0 ms"
        },
        "data": {"message": "Service is running"}
    }
