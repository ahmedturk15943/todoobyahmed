"""Unit tests for add_task MCP tool."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from backend.src.mcp.tools.add_task import add_task


@pytest.mark.asyncio
async def test_add_task_success():
    """Test successful task creation."""
    # Arrange
    user_id = "user_123"
    title = "Buy groceries"
    description = "Milk, eggs, bread"

    # Act
    result = await add_task(user_id=user_id, title=title, description=description)

    # Assert
    assert result["status"] == "created"
    assert result["title"] == title
    assert "task_id" in result
    assert isinstance(result["task_id"], int)


@pytest.mark.asyncio
async def test_add_task_empty_title():
    """Test that empty title raises ValueError."""
    # Arrange
    user_id = "user_123"
    title = ""

    # Act & Assert
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        await add_task(user_id=user_id, title=title)


@pytest.mark.asyncio
async def test_add_task_whitespace_only_title():
    """Test that whitespace-only title raises ValueError."""
    # Arrange
    user_id = "user_123"
    title = "   "

    # Act & Assert
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        await add_task(user_id=user_id, title=title)


@pytest.mark.asyncio
async def test_add_task_without_description():
    """Test task creation without description."""
    # Arrange
    user_id = "user_123"
    title = "Call mom"

    # Act
    result = await add_task(user_id=user_id, title=title)

    # Assert
    assert result["status"] == "created"
    assert result["title"] == title
    assert "task_id" in result


@pytest.mark.asyncio
async def test_add_task_title_too_long():
    """Test that title exceeding 255 characters raises ValueError."""
    # Arrange
    user_id = "user_123"
    title = "A" * 256  # 256 characters

    # Act & Assert
    with pytest.raises(ValueError, match="exceeds 255 characters"):
        await add_task(user_id=user_id, title=title)


@pytest.mark.asyncio
async def test_add_task_strips_whitespace():
    """Test that title whitespace is stripped."""
    # Arrange
    user_id = "user_123"
    title = "  Buy groceries  "

    # Act
    result = await add_task(user_id=user_id, title=title)

    # Assert
    assert result["title"] == "Buy groceries"
