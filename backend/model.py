import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def detect_language(code: str) -> str:
    """Detects the programming language based on syntax patterns."""
    if re.search(r'#include\s*<.*>', code) or re.search(r'\bint\s+main\s*\(', code):
        return "C" if "printf" in code else "C++"
    elif "import java" in code or "class " in code and "public static void main" in code:
        return "Java"
    elif "def " in code or "import " in code:
        return "Python"
    elif re.search(r'function\s+\w+\s*\(', code) or "=>" in code or "console.log" in code:
        return "JavaScript"
    elif re.search(r'\binterface\b|\btype\b', code) and ":" in code:
        return "TypeScript"
    else:
        return "Unknown"

def explain_code(code: str) -> str:
    """Generates an explanation of the given code in the detected programming language."""
    language = detect_language(code)

    if language == "Unknown":
        return "❌ Could not detect the programming language."

    prompt = f"""
    Explain the following {language} code in simple terms. 
    If there are mistakes, point them out. 

    Format:
    1. **Purpose:** What does the code do?
    2. **How it works:** Key steps in simple words.
    3. **Concepts used:** Mention only important ones.
    4. **Improvements:** (Only if needed, keep it short.)

    Code:
    ```{language}
    {code}
    ```
    Keep it **short, clear, and beginner-friendly**.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        explanation = response.text.strip() if response else "Explanation not available."
        return f"**Detected Language: {language}**\n\n{explanation}"
    except Exception as e:
        return f"API Error: {str(e)}"

def generate_test_cases(code: str) -> str:
    """Generates simple test cases based on the detected language and checks if the code is correct."""
    language = detect_language(code)

    if language == "Unknown":
        return "❌ Could not detect the programming language."

    prompt = f"""
    Analyze the following {language} code and determine if it works correctly.
    If there are any logical errors, mention them.

    Then, generate simple test cases in the following format:
    - **Input:** (if applicable)
    - **Expected Output:** (based on the function logic)

    Do not use any testing frameworks. Keep it **clean and readable**.

    Code:
    ```{language}
    {code}
    ```

    At the end, include:
    - **Code Status:** (Correct ✅ / Has Issues ❌)
    - **Issues (if any):** (If the code has problems, briefly describe them.)
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        test_cases = response.text.strip() if response else "Test cases not available."
        return f"**Detected Language: {language}**\n\n{test_cases}"
    except Exception as e:
        return f"API Error: {str(e)}"
