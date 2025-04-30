import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("AI-Based Code Explainer & Test Case Generator")

option = st.sidebar.selectbox("Choose Functionality", ["Code Explainer", "Test Case Generator"])

if option == "Code Explainer":
    st.subheader("Paste Code")
    
    code = st.text_area("Paste your code here")
    
    if st.button("Explain Code"):
        if code.strip():
            response = requests.post(f"{BACKEND_URL}/explain", json={"code": code})
            if response.status_code == 200:
                st.subheader("Explanation:")
                st.write(response.json()["explanation"])
            else:
                st.error("Error processing request")
        else:
            st.warning("Please enter valid Python code.")

elif option == "Test Case Generator":
    st.subheader("Paste Function Code")
    
    function_code = st.text_area("Paste your function code here")
    
    if st.button("Generate Test Cases"):
        if function_code.strip():
            response = requests.post(f"{BACKEND_URL}/generate_tests", json={"code": function_code})
            if response.status_code == 200:
                st.subheader("Generated Test Cases:")
                st.code(response.json()["test_cases"], language="python")
            else:
                st.error("Error processing request")
        else:
            st.warning("Please enter valid function code.")
