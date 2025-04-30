from fastapi import FastAPI
from pydantic import BaseModel
from model import explain_code, generate_test_cases

app = FastAPI()

class CodeRequest(BaseModel):
    code: str

@app.post("/explain")
async def explain_code_api(request: CodeRequest):
    explanation = explain_code(request.code)
    return {"explanation": explanation}

@app.post("/generate_tests")
async def generate_tests_api(request: CodeRequest):
    test_cases = generate_test_cases(request.code)
    return {"test_cases": test_cases}
