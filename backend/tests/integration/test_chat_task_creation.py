"""Integration test for chat endpoint task creation."""
import pytest
from httpx import AsyncClient
from backend.src.main import app


@pytest.mark.asyncio
async def test_chat_task_creation_end_to_end():
    """Test complete flow: user sends message, AI creates task, response returned."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Arrange
        user_id = "test_user_123"
        message = "Add a task to buy groceries"

        # Act
        response = await client.post(
            f"/api/{user_id}/chat",
            json={"message": message}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert "response" in data
        assert "tool_calls" in data
        assert isinstance(data["conversation_id"], int)


@pytest.mark.asyncio
async def test_chat_empty_message():
    """Test that empty message returns 400 error."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Arrange
        user_id = "test_user_123"
        message = ""

        # Act
        response = await client.post(
            f"/api/{user_id}/chat",
            json={"message": message}
        )

        # Assert
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_chat_continue_conversation():
    """Test continuing an existing conversation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Arrange
        user_id = "test_user_123"

        # First message - create conversation
        response1 = await client.post(
            f"/api/{user_id}/chat",
            json={"message": "Add a task to buy groceries"}
        )
        conversation_id = response1.json()["conversation_id"]

        # Act - Second message in same conversation
        response2 = await client.post(
            f"/api/{user_id}/chat",
            json={
                "conversation_id": conversation_id,
                "message": "Show me all my tasks"
            }
        )

        # Assert
        assert response2.status_code == 200
        data = response2.json()
        assert data["conversation_id"] == conversation_id


@pytest.mark.asyncio
async def test_chat_invalid_conversation_id():
    """Test that invalid conversation_id returns 400 error."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Arrange
        user_id = "test_user_123"
        invalid_conversation_id = 99999

        # Act
        response = await client.post(
            f"/api/{user_id}/chat",
            json={
                "conversation_id": invalid_conversation_id,
                "message": "Hello"
            }
        )

        # Assert
        assert response.status_code == 400
        assert "not found" in response.json()["detail"].lower()
