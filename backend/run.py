import uvicorn
from core.config import settings

uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)