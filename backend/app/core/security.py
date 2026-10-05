import hmac
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.app.core.config import get_settings

bearer_scheme = HTTPBearer(auto_error=False)


def require_demo_identity(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> str:
    settings = get_settings()
    if (
        credentials is None
        or not settings.demo_access_token
        or not hmac.compare_digest(credentials.credentials, settings.demo_access_token)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    if settings.app_env.lower() == "production":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Demo authentication is disabled in production",
        )
    return "cust_demo"