from fastapi import FastAPI

app = FastAPI()

EXPLANATIONS = {
    "input": "Correct usage of input() is required.",
    "output": "Your program must print results.",
    "pseudocode": "Include comments explaining your code.",
    "variables": "Use variables correctly.",
    "List or Dictionary": "Use lists/dictionaries where required.",
    "decision structure": "Use if/elif/else properly.",
    "structure(loops and decision structures)": "Use loops AND decisions.",
    "functions": "Define functions for modular code."
}

@app.get("/explain/{key}")
def explain(key: str):
    return {"explanation": EXPLANATIONS.get(key, "No explanation.")}