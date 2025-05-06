# app/main.py
from starlette.middleware.cors import CORSMiddleware
from controller import project_controller, skill_controller, person_controller

from fastapi import FastAPI

import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_controller.project_router, prefix="/projects", tags=["projects"])
app.include_router(skill_controller.skill_router, prefix="/skills", tags=["skills"])
app.include_router(person_controller.person_router, prefix="/persons", tags=["persons"])
# @app.on_event("startup")
# def on_startup():
#     init_db()  # 生产环境建议使用迁移工具

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=23333)