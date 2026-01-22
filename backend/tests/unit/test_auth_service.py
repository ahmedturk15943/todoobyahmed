"""Unit tests for authentication service."""

import pytest
from src.services.auth_service import AuthService
from src.models.user import User


@pytest.mark.unit
class TestAuthService:
    """Test authentication service methods."""

    def test_hash_password(self):
        """Test password hashing."""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)

        assert hashed != password
        assert len(hashed) > 0
        assert AuthService.verify_password(password, hashed)

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)

        assert AuthService.verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = AuthService.hash_password(password)

        assert AuthService.verify_password(wrong_password, hashed) is False

    def test_create_jwt_token(self):
        """Test JWT token creation."""
        import uuid
        user_id = uuid.uuid4()
        email = "test@example.com"

        token = AuthService.create_jwt_token(user_id, email)

        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)

    @pytest.mark.asyncio
    async def test_signup_success(self, test_session):
        """Test successful user signup."""
        email = "newuser@example.com"
        password = "password123"

        user, token = await AuthService.signup(email, password, test_session)

        assert user.email == email
        assert user.password_hash != password
        assert token is not None

    @pytest.mark.asyncio
    async def test_signup_duplicate_email(self, test_session):
        """Test signup with duplicate email."""
        email = "duplicate@example.com"
        password = "password123"

        # First signup should succeed
        await AuthService.signup(email, password, test_session)

        # Second signup with same email should fail
        with pytest.raises(ValueError, match="Email already registered"):
            await AuthService.signup(email, password, test_session)

    @pytest.mark.asyncio
    async def test_signup_invalid_email(self, test_session):
        """Test signup with invalid email."""
        with pytest.raises(ValueError, match="Invalid email format"):
            await AuthService.signup("invalidemail", "password123", test_session)

    @pytest.mark.asyncio
    async def test_signup_weak_password(self, test_session):
        """Test signup with weak password."""
        email = "test@example.com"

        # Too short
        with pytest.raises(ValueError, match="at least 8 characters"):
            await AuthService.signup(email, "short", test_session)

        # No letter
        with pytest.raises(ValueError, match="at least one letter"):
            await AuthService.signup(email, "12345678", test_session)

        # No number
        with pytest.raises(ValueError, match="at least one number"):
            await AuthService.signup(email, "password", test_session)
