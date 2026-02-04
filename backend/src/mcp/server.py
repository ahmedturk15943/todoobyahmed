"""MCP Server for AI Chatbot.

This module implements the Model Context Protocol (MCP) server that exposes
task management operations as tools for the AI agent.
"""
from typing import Dict, List, Any, Callable
import logging

logger = logging.getLogger(__name__)


class MCPServer:
    """
    MCP Server that manages tool registration and execution.

    Tools are stateless functions that the AI agent can invoke to perform
    task operations (add, list, complete, delete, update).
    """

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.tool_functions: Dict[str, Callable] = {}
        logger.info("MCP Server initialized")

    def register_tool(
        self,
        name: str,
        function: Callable,
        description: str,
        parameters: Dict[str, Any]
    ) -> None:
        """
        Register a tool with the MCP server.

        Args:
            name: Tool name (e.g., "add_task")
            function: The callable function to execute
            description: Human-readable description for the AI
            parameters: JSON schema for function parameters
        """
        self.tools[name] = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters
            }
        }
        self.tool_functions[name] = function
        logger.info(f"Registered tool: {name}")

    def get_tools(self) -> List[Dict[str, Any]]:
        """
        Get all registered tools in OpenAI function calling format.

        Returns:
            List of tool definitions
        """
        return list(self.tools.values())

    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Execute a registered tool.

        Args:
            name: Tool name to execute
            arguments: Tool arguments

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found
        """
        if name not in self.tool_functions:
            raise ValueError(f"Tool not found: {name}")

        logger.info(f"Executing tool: {name} with args: {arguments}")

        try:
            result = await self.tool_functions[name](**arguments)
            logger.info(f"Tool {name} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool {name} execution failed: {str(e)}")
            raise


# Global MCP server instance
mcp_server = MCPServer()


# Register tools
from .tools.add_task import add_task
from .tools.delete_task import delete_task
from .tools.complete_task import complete_task
from .tools.list_tasks import list_tasks

# Add task tool
mcp_server.register_tool(
    name="add_task",
    function=add_task,
    description="Create a new task for the user. Use this when the user wants to add, create, or remember something.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The authenticated user's identifier"
            },
            "title": {
                "type": "string",
                "description": "The task title (required, 1-255 characters)"
            },
            "description": {
                "type": "string",
                "description": "Optional detailed description of the task"
            }
        },
        "required": ["user_id", "title"]
    }
)

# Delete task tool
mcp_server.register_tool(
    name="delete_task",
    function=delete_task,
    description="Delete a task. Use this when the user wants to remove or delete a task. You must know the task_id to delete it.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The authenticated user's identifier"
            },
            "task_id": {
                "type": "integer",
                "description": "The ID of the task to delete"
            }
        },
        "required": ["user_id", "task_id"]
    }
)

# Complete task tool
mcp_server.register_tool(
    name="complete_task",
    function=complete_task,
    description="Mark a task as completed. Use this when the user wants to complete, finish, check off, or mark a task as done.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The authenticated user's identifier"
            },
            "task_id": {
                "type": "integer",
                "description": "The ID of the task to complete"
            }
        },
        "required": ["user_id", "task_id"]
    }
)

# List tasks tool
mcp_server.register_tool(
    name="list_tasks",
    function=list_tasks,
    description="Get a list of the user's tasks. Use this when the user wants to see their tasks, or when you need to find a task by name to get its ID.",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The authenticated user's identifier"
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of tasks to return (default 50)"
            }
        },
        "required": ["user_id"]
    }
)
