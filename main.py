
import sys
import subprocess
import tempfile
from pathlib import Path

from monitor.error_monitor import monitor_python_file
from agent.investigator import investigate_error


def display_report(file_path):
    """
    Execute a Python file, capture errors,
    and generate an AI investigation report.
    """

    print("\nPYTHON AI INVESTIGATOR")
    print("=" * 50)

    # Step 1: Execute Python file
    try:
        result = monitor_python_file(file_path)

    except subprocess.TimeoutExpired:
        print("Program exceeded the execution time limit.")
        return

    except (ValueError, OSError) as error:
        print("Monitor Error:", error)
        return

    print("\nReturn Code:", result["returncode"])

    # Step 2: Display normal output
    if result["stdout"]:
        print("\nPROGRAM OUTPUT:")
        print(result["stdout"])

    # Step 3: Check execution status
    if not result["has_error"]:
        print("\nProgram executed successfully.")
        return

    print("\nERROR DETECTED:")
    print(result["stderr"])

    # Step 4: Read Python source code
    source_code = Path(result["file"]).read_text(
        encoding="utf-8-sig",
        errors="replace"
    )

    # Step 5: Investigate with Ollama
    print("\nAI Investigator is analyzing the error...")

    explanation = investigate_error(
        source_code,
        result["stderr"]
    )

    # Step 6: Display explanation
    print("\nAI INVESTIGATION REPORT")
    print("=" * 50)
    print(explanation)


def enter_python_code():
    """
    Accept multiline Python code from the terminal.
    """

    print("\nEnter your Python code below.")
    print("Type END on a separate line when finished.\n")

    code_lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip() == "END":
            break

        code_lines.append(line)

    source_code = "\n".join(code_lines)

    if not source_code.strip():
        print("No Python code entered.")
        return

    # Create temporary Python file
    with tempfile.TemporaryDirectory() as temp_dir:

        temp_file = Path(temp_dir) / "user_code.py"

        temp_file.write_text(
            source_code,
            encoding="utf-8"
        )

        # Pass temporary file to existing monitor
        display_report(temp_file)


def select_python_file():
    """
    Accept an existing Python file path.
    """

    file_path = input(
        "\nEnter the Python file path: "
    ).strip().strip('"')

    if not file_path:
        print("No file path entered.")
        return

    display_report(file_path)


def main():
    """
    Main menu for Python AI Investigator.
    """

    while True:

        print("\n" + "=" * 50)
        print("       PYTHON AI INVESTIGATOR")
        print("=" * 50)

        print("1. Enter Python code")
        print("2. Select existing Python file")
        print("3. Exit")

        choice = input("\nChoose an option (1/2/3): ").strip()

        if choice == "1":
            enter_python_code()

        elif choice == "2":
            select_python_file()

        elif choice == "3":
            print("\nExiting Python AI Investigator.")
            break

        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
