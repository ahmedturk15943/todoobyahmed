# Test Phase 1 CLI Todo App
import subprocess
import sys
import io
import os
import shlex

# Fix Windows encoding issue with Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def run_command(cmd):
    """Run CLI command and return (exit_code, stdout, stderr)."""
    full_cmd = [sys.executable, "-m", "src.cli.main"] + shlex.split(cmd)
    result = subprocess.run(full_cmd, capture_output=True)
    # Decode bytes with utf-8, ignoring errors for Windows console compatibility
    stdout = result.stdout.decode('utf-8', errors='ignore')
    stderr = result.stderr.decode('utf-8', errors='ignore')
    return result.returncode, stdout, stderr


def print_result(success, message):
    status = "✓ PASS" if success else "✗ FAIL"
    color = "\033[32m" if success else "\033[31m"
    print(f"{color}{status}\033[0m - {message}")


def main():
    print("\n--- Phase I CLI Todo App Test ---\n")

    # Clear data file for clean test
    data_file = os.path.join(os.path.dirname(__file__), ".todo_data.json")
    if os.path.exists(data_file):
        os.remove(data_file)

    # 1. Add task
    code, out, err = run_command('add "Buy groceries" --description "Milk, eggs"')
    print_result(code == 0 and "Task created" in out, "Add task 1")

    # 2. Add another task
    code, out, err = run_command('add "Do homework" --description "Math assignment"')
    print_result(code == 0 and "Task created" in out, "Add task 2")

    # 3. List tasks
    code, out, err = run_command("list")
    success = "Buy groceries" in out and "Do homework" in out
    print_result(success, "List tasks")

    # 4. Complete first task
    code, out, err = run_command("complete 1")
    success = code == 0 and ("marked as complete" in out or "already marked" in out)
    print_result(success, "Complete task 1")

    # 5. Update second task
    code, out, err = run_command('update 2 --title "Do math homework"')
    success = code == 0 and "Task updated" in out
    print_result(success, "Update task 2")

    # 6. Delete first task
    code, out, err = run_command("delete 1")
    success = code == 0 and "Task deleted" in out
    print_result(success, "Delete task 1")

    # 7. List after deletion
    code, out, err = run_command("list")
    success = "Do math homework" in out and "Buy groceries" not in out
    print_result(success, "List after deletion")

    print("\n--- Tests Complete ---\n")


if __name__ == "__main__":
    main()
