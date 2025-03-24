from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.services.auth_service import KeycloakAuth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Security(oauth2_scheme)):
    keycloak = KeycloakAuth()
    try:
        user_info = keycloak.get_user_info(token)
        return user_info
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:  # 可扩展用户状态字段
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_admin:  # 需要添加管理员字段
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Requires admin privileges"
        )
    return current_user

def verify_project_owner(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.get(Project, project_id)
    if not project or project.creator_id != current_user.id:
        raise HTTPException(403, "Not authorized")
    return project