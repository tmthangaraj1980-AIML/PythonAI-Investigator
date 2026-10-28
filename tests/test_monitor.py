
from pathlib import Path

from monitor.error_monitor import monitor_python_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = PROJECT_ROOT / "Examples"


def test_zero_division_error():
    result = monitor_python_file(
        EXAMPLES / "zero_division.py"
    )

    assert result["has_error"] is True
    assert "ZeroDivisionError" in result["stderr"]


def test_name_error():
    result = monitor_python_file(
        EXAMPLES / "name_error.py"
    )

    assert result["has_error"] is True
    assert "NameError" in result["stderr"]
    assert "Arun" in result["stdout"]


def test_type_error():
    result = monitor_python_file(
        EXAMPLES / "type_error.py"
    )

    assert result["has_error"] is True
    assert "TypeError" in result["stderr"]


def test_successful_execution():
    result = monitor_python_file(
        EXAMPLES / "success.py"
    )

    assert result["has_error"] is False
    assert result["returncode"] == 0
    assert "Result: 15" in result["stdout"]


def test_syntax_error():
    result = monitor_python_file(
        EXAMPLES / "syntax_error.py"
    )

    assert result["has_error"] is True
    assert "SyntaxError" in result["stderr"]
