"""Authentication service for user signup, signin, and JWT management."""

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import Optional

from ..models.user import User, UserPublic
from ..config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_jwt_token(user_id: uuid.UUID, email: str) -> str:
        """Create a JWT token for a user."""
        expiry = datetime.utcnow() + timedelta(days=settings.jwt_expiry_days)
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expiry,
            "iat": datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.better_auth_secret, algorithm=settings.jwt_algorithm)
        return token

    @staticmethod
    async def signup(email: str, password: str, session: AsyncSession) -> tuple[User, str]:
        """
        Create a new user account.

        Args:
            email: User's email address
            password: Plain text password
            session: Database session

        Returns:
            Tuple of (User, JWT token)

        Raises:
            ValueError: If email already exists or validation fails
        """
        # Validate email format
        if "@" not in email or "." not in email.split("@")[1]:
            raise ValueError("Invalid email format")

        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isalpha() for c in password):
            raise ValueError("Password must contain at least one letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one number")

        # Check if email already exists
        result = await session.execute(select(User).where(User.email == email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise ValueError("Email already registered")

        # Create new user
        password_hash = AuthService.hash_password(password)
        user = User(email=email, password_hash=password_hash)
        session.add(user)
        await session.commit()
        await session.refresh(user)

        # Create JWT token
        token = AuthService.create_jwt_token(user.id, user.email)

        return user, token

    @staticmethod
    async def signin(email: str, password: str, session: AsyncSession) -> tuple[User, str]:
        """
        Authenticate a user and return JWT token.

        Args:
            email: User's email address
            password: Plain text password
            session: Database session

        Returns:
            Tuple of (User, JWT token)

        Raises:
            ValueError: If credentials are invalid
        """
        # Find user by email
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        if not AuthService.verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        # Create JWT token
        token = AuthService.create_jwt_token(user.id, user.email)

        return user, token
