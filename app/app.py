import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.controller import blog_controller
from app.config.config import settings
from app.config.logging_config import setup_logging
from app.controller import project_controller, skill_controller, person_controller

# app = FastAPI()
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 初始化日志
setup_logging()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)


# 添加中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("request")
    logger.info(f"Request: {request.method} {request.url}")

    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error(f"Request failed: {exc}")
        raise

    logger.info(f"Response status: {response.status_code}")
    return response


# 全局异常处理
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger = logging.getLogger("exception")
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger = logging.getLogger("exception")
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


# 示例路由
@app.get("/")
async def root():
    logger = logging.getLogger(__name__)
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}


app.include_router(project_controller.project_router, prefix="/projects", tags=["projects"])
app.include_router(skill_controller.skill_router, prefix="/skills", tags=["skills"])
app.include_router(person_controller.person_router, prefix="/persons", tags=["persons"])

app.include_router(blog_controller.blog_router, prefix="/blog", tags=["blog"])
# @app.on_event("startup")
# def on_startup():
#     init_db()  # 生产环境建议使用迁移工具

