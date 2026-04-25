import ast
import re
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return {}

    func_docstrings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            if doc:
                func_docstrings.append({"function": node.name, "docstring": doc.strip()})

    business_rules = re.findall(r"#\s*(Business Logic Rule\s*\d+.*)", source_code, flags=re.IGNORECASE)
    vat_comment_mentions_8 = bool(re.search(r"8\s*%", source_code))
    vat_code_mentions_10 = bool(re.search(r"tax_rate\s*=\s*0\.10", source_code))

    content_parts = [f"{item['function']}: {item['docstring']}" for item in func_docstrings]
    if business_rules:
        content_parts.append("Rules in comments: " + " | ".join(business_rules))
    content = "\n".join(content_parts).strip()

    return {
        "document_id": "legacy-code-001",
        "content": content,
        "source_type": "Code",
        "author": "Legacy Senior Dev",
        "timestamp": datetime.utcnow().isoformat(),
        "source_metadata": {
            "original_file": "legacy_pipeline.py",
            "docstring_count": len(func_docstrings),
            "functions_with_docstrings": [item["function"] for item in func_docstrings],
            "business_rules_in_comments": business_rules,
            "vat_comment_mentions_8_percent": vat_comment_mentions_8,
            "vat_code_mentions_10_percent": vat_code_mentions_10,
        },
    }

