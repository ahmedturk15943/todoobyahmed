"""Authentication routes for signup, signin, and signout."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import SessionDep
from ..models.auth import SignUpRequest, SignInRequest, AuthResponse, UserResponse
from ...services.auth_service import AuthService


router = APIRouter()


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignUpRequest, session: SessionDep):
    """
    Create a new user account.

    Args:
        request: Signup request with email and password
        session: Database session

    Returns:
        AuthResponse with user data and JWT token

    Raises:
        HTTPException: If email already exists or validation fails
    """
    try:
        user, token = await AuthService.signup(request.email, request.password, session)

        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at,
            ),
            token=token,
            message="Account created successfully",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/signin", response_model=AuthResponse)
async def signin(request: SignInRequest, session: SessionDep):
    """
    Authenticate user and return JWT token.

    Args:
        request: Signin request with email and password
        session: Database session

    Returns:
        AuthResponse with user data and JWT token

    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        user, token = await AuthService.signin(request.email, request.password, session)

        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at,
            ),
            token=token,
            message="Signed in successfully",
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/signout")
async def signout():
    """
    Sign out user (client-side token removal).

    Note: JWT tokens are stateless, so signout is handled client-side
    by removing the token from storage.

    Returns:
        Success message
    """
    return {"message": "Signed out successfully"}
