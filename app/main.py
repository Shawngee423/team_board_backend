# app/main.py
from app.controller.project_controller import project_router
from app.controller.skill_controller import skill_router
from app.controller.user_controller import user_router
from app.database import init_db

from fastapi import FastAPI, Depends
from app.auth.dependency import get_current_user

import uvicorn

app = FastAPI()
app.include_router(user_router)
app.include_router(skill_router)
app.include_router(project_router)

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['preferred_username']}"}


@app.on_event("startup")
def on_startup():
    init_db()  # 生产环境建议使用迁移工具


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=23333)