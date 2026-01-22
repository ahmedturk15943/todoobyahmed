"""JWT authentication middleware for protecting API routes."""

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional
import uuid

from ...config import settings


security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> uuid.UUID:
    """
    Extract and verify JWT token, return user ID.

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.jwt_algorithm]
        )

        # Extract user ID from payload
        user_id_str: Optional[str] = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token: missing user ID",
            )

        # Convert to UUID
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token: invalid user ID format",
            )

        return user_id

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
        )


async def verify_user_access(
    user_id_from_path: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user_id)
) -> uuid.UUID:
    """
    Verify that the authenticated user matches the user ID in the path.

    This prevents users from accessing other users' resources.

    Args:
        user_id_from_path: User ID from the URL path
        current_user_id: User ID from JWT token

    Returns:
        The verified user ID

    Raises:
        HTTPException: If user IDs don't match (403 Forbidden)
    """
    if user_id_from_path != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )

    return current_user_id
