
from agent.investigator import investigate_error

source_code = """
a = 10
b = 0
print(a / b)
"""

traceback_text = """
ZeroDivisionError: division by zero
"""

explanation = investigate_error(
    source_code,
    traceback_text
)

print("\nPYTHON AI INVESTIGATOR REPORT")
print("=" * 50)
print(explanation)
