from fastapi import HTTPException
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError
from sqlmodel import Session

from app.config.config import settings
from app.services.user_service import get_user_by_keycloak_id, create_user
from app.models.user import User, UserCreate


class KeycloakAuth:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.oidc = KeycloakOpenID(
                server_url=settings.KEYCLOAK_URL,
                client_id=settings.KEYCLOAK_CLIENT_ID,
                realm_name=settings.KEYCLOAK_REALM,
                client_secret_key=settings.KEYCLOAK_CLIENT_SECRET
            )
        return cls._instance

    async def get_user_info(self, token: str):
        return self.oidc.userinfo(token)

    async def introspect_token(self, token: str):
        return self.oidc.introspect(token)

    async def sync_user(self, token: str, db: Session) -> User:
        try:
            user_info = await self.get_user_info(token)

            # 查找或创建用户
            user = get_user_by_keycloak_id(db, user_info['sub'])
            if not user:
                user_data = UserCreate(
                    keycloak_id=user_info['sub'],
                    username=user_info['preferred_username'],
                    email=user_info.get('email', ''),
                    full_name=user_info.get('name', ''),
                    skill_ids=[]  # 初始无技能
                )
                user = create_user(db, user_data)
            return user
        except KeycloakAuthenticationError as e:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials"
            )