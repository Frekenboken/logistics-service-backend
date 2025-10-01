from src.core.config import settings

from authx import AuthX, AuthXConfig
from authx.exceptions import MissingTokenError

from fastapi import HTTPException, status

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.SECRET_KEY
config.JWT_ACCESS_CSRF_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

async def access_token_required():
    try:
        return security.access_token_required
    except MissingTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )