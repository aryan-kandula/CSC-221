"""
Helper functions for analyzing Python code submissions
Used by grader.py to evaluate student code
"""
import ast
import re


def safe_parse_python(src):
    """
    Check if Python code has valid syntax
    Returns True if code can be parsed, False otherwise
    """
    try:
        ast.parse(src)
        return True
    except:
        return False


def contains_while_true(src):
    """
    Detect if code contains 'while True' or 'while 1' loops
    Returns True if found (which is not allowed per requirements)
    """
    # Convert to lowercase for case-insensitive matching
    s = src.lower()
    
    # Check for various forms of infinite loops
    patterns = [
        "while true",
        "while 1",
        "while(true)",
        "while(1)",
        "while 1:",
        "while true:"
    ]
    
    return any(pattern in s for pattern in patterns)


def count_comments(src):
    """
    Count the number of comment lines in code
    Used to evaluate pseudocode/documentation
    """
    # Count lines that start with # (after stripping whitespace)
    lines = src.split('\n')
    comment_count = sum(1 for line in lines if line.strip().startswith('#'))
    
    # Also count docstrings
    docstring_count = src.count('"""') // 2 + src.count("'''") // 2
    
    return comment_count + docstring_count


def count_assignments(src):
    """
    Count variable assignments in code
    Used to evaluate proper use of variables
    """
    # Pattern matches variable assignments (basic form)
    # Looks for: word = something
    pattern = r'\b\w+\s*=\s*'
    assignments = re.findall(pattern, src)
    
    # Filter out comparison operators (==, !=, <=, >=)
    valid_assignments = [a for a in assignments if not any(op in a for op in ['==', '!=', '<=', '>='])]
    
    return len(valid_assignments)


def has_input_call(src):
    """
    Check if code contains input() function calls
    """
    return "input(" in src


def has_print_call(src):
    """
    Check if code contains print() function calls
    """
    return "print(" in src


def has_list_or_dict(src):
    """
    Check if code uses lists or dictionaries
    Looks for [ ] or { } characters
    """
    # Check for list literals
    has_list = "[" in src and "]" in src
    
    # Check for dictionary literals
    has_dict = "{" in src and "}" in src
    
    return has_list or has_dict


def has_decision_structure(src):
    """
    Check if code contains decision structures (if/elif/else)
    """
    keywords = ["if ", "elif ", "else"]
    return any(keyword in src for keyword in keywords)


def has_loop_or_structure(src):
    """
    Check if code contains loops (for/while) or decision structures
    """
    s = src.lower()
    keywords = ["for ", "while ", "if "]
    return any(keyword in s for keyword in keywords)


def has_function_def(src):
    """
    Check if code defines at least one function
    """
    return "def " in src


def count_functions(src):
    """
    Count the number of function definitions in code
    """
    return src.count("def ")


def has_loop(src):
    """
    Check if code contains any loop structure
    """
    s = src.lower()
    return "for " in s or "while " in s


def count_loops(src):
    """
    Count the number of loop structures
    """
    s = src.lower()
    for_count = s.count("for ")
    while_count = s.count("while ")
    return for_count + while_count


def get_code_metrics(src):
    """
    Return a dictionary of various code metrics
    Useful for detailed analysis
    """
    return {
        'valid_syntax': safe_parse_python(src),
        'has_while_true': contains_while_true(src),
        'comment_count': count_comments(src),
        'assignment_count': count_assignments(src),
        'has_input': has_input_call(src),
        'has_print': has_print_call(src),
        'has_collections': has_list_or_dict(src),
        'has_decisions': has_decision_structure(src),
        'has_loops': has_loop(src),
        'function_count': count_functions(src),
        'loop_count': count_loops(src),
        'line_count': len(src.split('\n'))
    }