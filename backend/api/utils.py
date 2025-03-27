import time
from core.config import settings

def format_response(data, start_time, success=True, message="success", debug=False):
    duration_ms = f"{int((time.time() - start_time) * 1000)} ms"
    return {
        "status": {
            "is_good": success,
            "message": message,
            "debug": debug,
            "env": settings.ENVIRONMENT,
            "duration": duration_ms
        },
        "data": data
    }