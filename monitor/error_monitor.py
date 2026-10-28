
import subprocess
import sys
from pathlib import Path


def monitor_python_file(file_path):
    """
    Execute a Python file and capture its output.
    """

    path = Path(file_path).resolve()

    if not path.is_file() or path.suffix.lower() != ".py":
        raise ValueError("Please provide a valid Python file.")

    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=path.parent
    )

    return {
        "file": str(path),
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
        "has_error": result.returncode != 0
    }
