"""Contract test for chat API against OpenAPI specification."""
import pytest
from httpx import AsyncClient
import yaml
from pathlib import Path
from backend.src.main import app


@pytest.fixture
def openapi_spec():
    """Load OpenAPI specification."""
    spec_path = Path(__file__).parent.parent.parent.parent / "specs" / "001-ai-chatbot-mcp" / "contracts" / "chat-api.yaml"
    with open(spec_path, 'r') as f:
        return yaml.safe_load(f)


@pytest.mark.asyncio
async def test_chat_endpoint_request_schema(openapi_spec):
    """Test that chat endpoint accepts requests matching OpenAPI schema."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Arrange - Valid request per OpenAPI spec
        user_id = "test_user"
        request_data = {
            "message": "Add a task to buy groceries"
        }

        # Act
        response = await client.post(
            f"/api/{user_id}/chat",
            json=request_data
        )

        # Assert - Should accept valid request
        assert response.status_code in [200, 201]


@pytest.mark.asyncio
async def test_chat_endpoint_response_schema(openapi_spec):
    """Test that chat endpoint returns response matching OpenAPI schema."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Arrange
        user_id = "test_user"
        request_data = {"message": "Hello"}

        # Act
        response = await client.post(
            f"/api/{user_id}/chat",
            json=request_data
        )

        # Assert - Response matches schema
        assert response.status_code == 200
        data = response.json()

        # Required fields per OpenAPI spec
        assert "conversation_id" in data
        assert "response" in data
        assert "tool_calls" in data

        # Type validation
        assert isinstance(data["conversation_id"], int)
        assert isinstance(data["response"], str)
        assert isinstance(data["tool_calls"], list)


@pytest.mark.asyncio
async def test_chat_endpoint_error_responses(openapi_spec):
    """Test that error responses match OpenAPI specification."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test 400 Bad Request
        response = await client.post(
            "/api/test_user/chat",
            json={"message": ""}  # Empty message
        )

        assert response.status_code == 400
        error_data = response.json()
        assert "detail" in error_data  # Error format per spec


@pytest.mark.asyncio
async def test_chat_endpoint_optional_conversation_id(openapi_spec):
    """Test that conversation_id is optional per OpenAPI spec."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Without conversation_id
        response1 = await client.post(
            "/api/test_user/chat",
            json={"message": "Hello"}
        )
        assert response1.status_code == 200

        # With conversation_id
        conversation_id = response1.json()["conversation_id"]
        response2 = await client.post(
            "/api/test_user/chat",
            json={
                "conversation_id": conversation_id,
                "message": "Hello again"
            }
        )
        assert response2.status_code == 200
