import streamlit as st
import io
import time
import matplotlib.pyplot as plt
from contextlib import redirect_stdout, redirect_stderr
from flake8.api import legacy as flake8

def analyze_code(code):
    """
    Analyze the code using flake8 and return the formatted issues.
    """
    with io.StringIO(code) as f:
        checker = flake8.get_style_guide(ignore=['E501'], max_line_length=100)
        report = checker.check_files([f.name])
        report_string_io = io.StringIO()
        checker.report(report, report_string_io)
        report_string_io.seek(0)
        return report_string_io.read(), report.get_statistics('E'), report.get_statistics('W')

def execute_code(code):
    """
    Executes the provided code and measures execution time and captures output.
    """
    local_ns = {}
    with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
        start_time = time.perf_counter()
        exec(code, {"__builtins__": __builtins__}, local_ns)
        end_time = time.perf_counter()
        output = buf.getvalue()
    exec_time = end_time - start_time
    return exec_time, output

def plot_execution_time(exec_time):
    """
    Creates a simple bar chart showing the execution time.
    """
    fig, ax = plt.subplots()
    ax.barh(['Execution Time'], [exec_time], color='skyblue')
    ax.set_xlabel('Seconds')
    ax.set_title('Code Execution Time')
    st.pyplot(fig)

def app():
    st.title("Python Code Analyzer with flake8 and Performance Evaluator")

    code_file = st.file_uploader("Upload a Python file (.py)", type=["py"])
    
    if code_file is not None:
        code_content = code_file.getvalue().decode("utf-8")
        st.code(code_content)  # Display the uploaded code

        if st.button("Analyze and Execute Code"):
            # Analyze code using flake8
            analysis_results, errors, warnings = analyze_code(code_content)
            if analysis_results:
                st.text("Flake8 Analysis Results:")
                st.text_area("Issues found (scroll for more)", analysis_results, height=150)
                if errors:
                    st.error(f"Errors found: {len(errors)}")
                if warnings:
                    st.warning(f"Warnings found: {len(warnings)}")
            else:
                st.success("No style or syntax issues found!")

            # Execute code and measure performance
            exec_time, output = execute_code(code_content)
            st.write("Execution Results:")
            st.text_area("Execution Output", output, height=150)
            st.write(f"Execution Time: {exec_time:.4f} seconds")
            plot_execution_time(exec_time)

if __name__ == "__main__":
    app()
