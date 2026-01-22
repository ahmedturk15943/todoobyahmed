"""
CLI interface for Todo Application - Phase I (In-Memory Console App).

Provides command-line interface with subcommands for:
- add: Add new task
- list: View all tasks
- update: Update task details
- delete: Delete task
- complete: Mark task as complete
- help: Show usage information
"""
import argparse
import sys
import io
from src.services.todo_service import TodoService

# Fix Windows encoding issue with Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def print_success(message: str) -> None:
    """Print success message with checkmark."""
    print(f"\033[32m✓ {message}\033[0m")


def print_error(message: str) -> None:
    """Print error message with x mark."""
    print(f"\033[31m✗ Error: {message}\033[0m")


def print_task_list(tasks) -> None:
    """
    Display tasks in table format with status indicators.

    Args:
        tasks: List of Task objects to display
    """
    if not tasks:
        print("No tasks found. Add a task to get started.")
        return

    # Calculate column widths for alignment
    max_id_width = len("ID")
    max_title_width = max((len(str(task.title)) for task in tasks), default=0)
    max_title_width = max(max_title_width, len("Title"))
    max_desc_width = max((len(task.description[:50]) for task in tasks if task.description), default=0)
    max_desc_width = max(max_desc_width, len("Description"))
    max_status_width = len("Status")

    # Print header
    print()
    header = f"| {str('ID').ljust(max_id_width)} | {str('Title').ljust(max_title_width)} | {str('Description').ljust(max_desc_width)} | {str('Status').ljust(max_status_width)} |"
    separator = f"|{'-' * (max_id_width + 2)}|{'-' * (max_title_width + 2)}|{'-' * (max_desc_width + 2)}|{'-' * (max_status_width + 2)}|"
    print(header)
    print(separator)

    # Print each task
    for task in tasks:
        # Truncate long descriptions
        display_desc = task.description[:50] + "..." if len(task.description) > 50 else task.description

        # Status indicator
        status_indicator = "\033[32m✓\033[0m" if task.is_complete() else "\033[31m✗\033[0m"
        status_text = "complete" if task.is_complete() else "incomplete"

        row = f"| {str(task.id).ljust(max_id_width)} | {str(task.title).ljust(max_title_width)} | {display_desc.ljust(max_desc_width)} | {status_indicator} {status_text.ljust(max_status_width)} |"
        print(row)

    print(separator)
    print(f"Total: {len(tasks)} task(s)")


def cmd_add(args) -> None:
    """Handle 'add' command - create new task."""
    try:
        task = service.add(title=args.title, description=args.description or "")
        print_success(f"Task created: {task.title}")
    except ValueError as e:
        print_error(str(e))


def cmd_list(args) -> None:
    """Handle 'list' command - display all tasks."""
    tasks = service.list_all()
    print_task_list(tasks)


def cmd_update(args) -> None:
    """Handle 'update' command - update task details."""
    try:
        if args.title is None and args.description is None:
            print_error("At least title or description must be provided")
            return

        task = service.update(
            task_id=args.id,
            title=args.title,
            description=args.description
        )
        print_success(f"Task updated: {task.title}")
    except ValueError as e:
        print_error(str(e))


def cmd_delete(args) -> None:
    """Handle 'delete' command - remove task."""
    try:
        task = service.get_by_id(args.id)
        task_title = task.title if task else f"ID {args.id}"
        service.delete(args.id)
        print_success(f"Task deleted: {task_title}")
    except ValueError as e:
        print_error(str(e))


def cmd_complete(args) -> None:
    """Handle 'complete' command - mark task as complete."""
    try:
        task = service.mark_complete(args.id)
        if task.is_complete():
            print(f"Task {args.id} already marked as complete")
        else:
            print_success(f"Task {args.id} marked as complete")
    except ValueError as e:
        print_error(str(e))


def main():
    """Main CLI entry point - parse arguments and dispatch to appropriate command."""
    parser = argparse.ArgumentParser(
        description="Todo Application - Phase I (In-Memory Console App)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Brief task name (required)", nargs="?")
    add_parser.add_argument("--description", "-d", help="Detailed task information (optional)", default="")

    # List command
    list_parser = subparsers.add_parser("list", help="View all tasks")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update task details")
    update_parser.add_argument("id", help="Task ID to update (required)", type=int)
    update_parser.add_argument("--title", "-t", help="New title for the task (optional)")
    update_parser.add_argument("--description", "-d", help="New description for the task (optional)")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete task by ID")
    delete_parser.add_argument("id", help="Task ID to delete (required)", type=int)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task complete")
    complete_parser.add_argument("id", help="Task ID to mark complete (required)", type=int)

    # Help command
    subparsers.add_parser("help", help="Show this help message")

    # Parse arguments
    args = parser.parse_args()

    # Dispatch to appropriate command
    try:
        if args.command == "add":
            cmd_add(args)
        elif args.command == "list":
            cmd_list(args)
        elif args.command == "update":
            cmd_update(args)
        elif args.command == "delete":
            cmd_delete(args)
        elif args.command == "complete":
            cmd_complete(args)
        elif args.command == "help":
            parser.print_help()
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


# Initialize service
service = TodoService()

# Run main if executed directly
if __name__ == "__main__":
    main()
