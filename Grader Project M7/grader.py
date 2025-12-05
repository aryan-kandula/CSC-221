import os
import pandas as pd
from functions import *

# CRITERIA MAP - EXACTLY as per module_criterias-1.docx
CRITERIA_MAP = {
    "M1": {"input": 30, "output": 50, "pseudocode": 10, "variables": 5},
    "M2": {"input": 10, "output": 30, "List or Dictionary": 45, "pseudocode": 10, "variables": 5},
    "M3": {"input": 15, "decision structure": 25, "output": 45, "pseudocode": 10, "variables": 5},
    "M4": {"structure(loops and decision structures)": 40, "output": 40, "pseudocode": 5, "variables": 5},
    "M5": {"structure(loops and decision structures)": 30, "output": 50, "functions": 10, "pseudocode": 5, "variables": 5}
}

LOCAL_EXPLAIN = {
    "input": "🔌 Missing or incorrect input() usage - Your program needs to accept user input!",
    "output": "🖨️ Output (print) missing or incomplete - Make sure to display results to the user!",
    "pseudocode": "💬 Add comments describing your logic - Help others understand your code!",
    "variables": "🔤 Use more variables / better naming - Clear variable names improve readability!",
    "List or Dictionary": "📚 Collections not used where required - Lists or dictionaries are needed here!",
    "decision structure": "🔀 Missing if/elif/else branching - Add conditional logic to handle different cases!",
    "structure(loops and decision structures)": "🔄 Missing loop or structure logic - Use loops and decisions together!",
    "functions": "🔧 You must define at least one function - Break your code into reusable pieces!"
}

def get_local_explanation(key):
    return LOCAL_EXPLAIN.get(key, "❌ No explanation available.")


def _auto_fail(reason, criteria, content):
    """Returns a grade of 1 with specific failure reason"""
    fail = {k: 0 for k in criteria}
    return {
        **fail,
        "total_grade": 1,
        "feedback": {"general": reason},
        "snippet": content[:400],
        "failed": True
    }


def _score(content, criteria):
    # Check for while True first - immediate fail with grade 1
    if contains_while_true(content):
        return _auto_fail(
            "🚫 WHILE TRUE DETECTED! 🚫\n\n"
            "Whoa there, cowboy! 🤠 Your code contains 'while True' which creates an infinite loop. "
            "We can't have that in our graded assignments! "
            "Try using a different loop structure with a proper exit condition.\n\n"
            "Grade: 1/100 - Please revise and resubmit! 🔄",
            criteria,
            content
        )
    
    # Check for syntax errors - program crashes
    if not safe_parse_python(content):
        return _auto_fail(
            "❌ PROGRAM CRASHED! ❌\n\n"
            "Houston, we have a problem! 🚀 Your program has a syntax error and crashed. "
            "Please check your code for missing colons, parentheses, or other syntax issues.\n\n"
            "Grade: 1/100 - Fix the errors and try again! 🔧",
            criteria,
            content
        )

    # Calculate raw scores for each criterion
    raw = {
        "input": 100 if has_input_call(content) else 0,
        "output": 100 if has_print_call(content) else 0,
        "pseudocode": min(count_comments(content) * 10, 100),
        "variables": min(count_assignments(content) * 10, 100),
        "List or Dictionary": 100 if has_list_or_dict(content) else 0,
        "decision structure": 100 if has_decision_structure(content) else 0,
        "structure(loops and decision structures)": 100 if has_loop_or_structure(content) else 0,
        "functions": 100 if has_function_def(content) else 0
    }

    # Generate feedback ONLY for criteria in this module
    feedback = {}
    for crit in criteria.keys():
        val = raw.get(crit, 0)
        if val == 0:
            feedback[crit] = LOCAL_EXPLAIN.get(crit, "❌ Missing requirement")
        elif val < 50:
            feedback[crit] = f"⚠️ Needs improvement - Score: {val}/100"
        elif val < 80:
            feedback[crit] = f"👍 Good work! - Score: {val}/100"
        else:
            feedback[crit] = f"✅ Excellent! - Score: {val}/100"

    # Calculate weighted scores ONLY for this module's criteria
    weighted = {crit: round(raw[crit] * w / 100, 2) for crit, w in criteria.items()}
    total = round(sum(weighted.values()), 2)

    # Ensure minimum grade of 1 (not 0)
    if total <= 0:
        total = 1
        feedback["general"] = "⚠️ No criteria met - Please review requirements and resubmit."

    return {
        **weighted,
        "total_grade": total,
        "feedback": feedback,
        "snippet": content[:400],
        "failed": False
    }


def grade_folder(folder_path, criteria):
    """Grade all Python files in the specified folder"""
    rows = []
    feedback = []

    python_files_found = False
    
    for root, _, files in os.walk(folder_path):
        for f in files:
            if f.endswith(".py"):
                python_files_found = True
                path = os.path.join(root, f)
                try:
                    content = open(path, "r", encoding="utf-8").read()
                except:
                    content = ""

                result = _score(content, criteria)
                result["file"] = f

                # Build row for DataFrame
                row = {
                    "file": f,
                    **{k: result[k] for k in criteria},
                    "total_grade": result["total_grade"]
                }
                rows.append(row)
                feedback.append(result)

    # Handle case where no Python files are found
    if not python_files_found:
        empty_row = {
            "file": "No files found",
            **{k: 0 for k in criteria},
            "total_grade": 0
        }
        rows.append(empty_row)
        feedback.append({
            **{k: 0 for k in criteria},
            "file": "No files found",
            "total_grade": 0,
            "feedback": {"general": "⚠️ No Python files found in the uploaded ZIP!"},
            "snippet": "",
            "failed": False
        })

    df = pd.DataFrame(rows)
    return df, feedback