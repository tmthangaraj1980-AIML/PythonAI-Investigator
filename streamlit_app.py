
import tempfile
from pathlib import Path

import streamlit as st

from monitor.error_monitor import monitor_python_file
from agent.investigator import investigate_error


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Python AI Investigator",
    page_icon="🔍",
    layout="wide"
)


# -------------------------------------------------
# APPLICATION HEADER
# -------------------------------------------------

st.title("🔍 Python AI Investigator")

st.write(
    "An AI-powered Python debugging and "
    "learning assistant."
)

st.info(
    "Local prototype: Run only Python code "
    "that you wrote or trust."
)


# -------------------------------------------------
# USER INPUT
# -------------------------------------------------

input_mode = st.radio(
    "Choose input method:",
    ["Enter Python Code", "Upload Python File"],
    horizontal=True
)

source_code = ""

if input_mode == "Enter Python Code":

    source_code = st.text_area(
        "Python Code Editor",
        value=(
            "numbers = [10, 20, 30]\n"
            "print(numbers[5])"
        ),
        height=250
    )

else:

    uploaded_file = st.file_uploader(
        "Upload a Python file",
        type=["py"]
    )

    if uploaded_file is not None:

        source_code = uploaded_file.getvalue().decode(
            "utf-8-sig",
            errors="replace"
        )

        st.code(
            source_code,
            language="python"
        )


# -------------------------------------------------
# ANALYZE BUTTON
# -------------------------------------------------

if st.button(
    "Analyze Python Code",
    type="primary"
):

    if not source_code.strip():

        st.warning(
            "Please enter or upload Python code."
        )

    else:

        # Create a temporary Python file
        with tempfile.TemporaryDirectory() as temp_dir:

            temp_file = Path(temp_dir) / "user_code.py"

            temp_file.write_text(
                source_code,
                encoding="utf-8"
            )

            # Execute using existing monitor
            try:
                with st.spinner("Executing Python code..."):
                    result = monitor_python_file(temp_file)

            except Exception as error:
                st.error(
                    f"Execution monitor failed: {error}"
                )
                st.stop()

        # -----------------------------------------
        # EXECUTION RESULTS
        # -----------------------------------------

        st.subheader("Execution Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Return Code",
                str(result["returncode"])
            )

        with col2:
            st.metric(
                "Error Detected",
                str(result["has_error"])
            )

        # -----------------------------------------
        # NORMAL PROGRAM OUTPUT
        # -----------------------------------------

        if result["stdout"]:

            st.subheader("Program Output")

            st.code(
                result["stdout"],
                language="text"
            )

        # -----------------------------------------
        # ERROR INVESTIGATION
        # -----------------------------------------

        if result["has_error"]:

            st.error("Python execution failed.")

            st.subheader("Error Traceback")

            st.code(
                result["stderr"],
                language="text"
            )

            with st.spinner(
                "AI Investigator is analyzing the error..."
            ):

                explanation = investigate_error(
                    source_code,
                    result["stderr"]
                )

            st.subheader("AI Investigation Report")

            st.markdown(explanation)

        else:

            st.success(
                "Program executed successfully. "
                "No errors detected."
            )
