import uvicorn
from app.config.config import settings
from app.app import app # noqa

if __name__ == '__main__':
    # uvicorn.run("main:app", host='0.0.0.0', port=23333)

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )