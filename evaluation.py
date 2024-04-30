import streamlit as st
import timeit
import io
import contextlib
import matplotlib.pyplot as plt
import numpy as np

def execute_and_time(code, local_namespace):
    """
    Execute the given code and measure execution time.
    """
    with io.StringIO() as buf, contextlib.redirect_stdout(buf):
        start_time = timeit.default_timer()
        exec(code, {}, local_namespace)
        end_time = timeit.default_timer()
        output = buf.getvalue()
    return local_namespace, end_time - start_time, output

def plot_metrics(metrics):
    """
    Generates a bar plot for the given metrics dictionary.
    """
    if metrics and isinstance(metrics, dict):
        fig, ax = plt.subplots()
        keys = list(metrics.keys())
        values = [metrics[key] for key in keys]
        ax.bar(keys, values, color='blue')
        ax.set_xlabel('Metrics')
        ax.set_ylabel('Values')
        ax.set_title('Evaluation Metrics')
        st.pyplot(fig)
    else:
        st.error("Metrics data is not in the expected format.")

def app():
    st.title("Python Code Analyzer")
    st.subheader("Upload your Python script for analysis and evaluation.")
    
    code_file = st.file_uploader("Upload a Python file (.py)", type=["py"])
    if code_file is not None:
        code_content = code_file.getvalue().decode("utf-8")
        st.code(code_content)

        if st.button("Analyze and Execute"):
            local_namespace = {}
            try:
                local_namespace, exec_time, output = execute_and_time(code_content, local_namespace)
                st.success(f"Executed in {exec_time:.4f} seconds")
                st.text_area("Output", output, height=300)
                
                if 'evaluate' in local_namespace:
                    metrics = local_namespace['evaluate']()
                    st.json(metrics)
                    plot_metrics(metrics)
            except Exception as e:
                st.error(f"Error executing the Python code: {e}")

if __name__ == "__main__":
    app()
