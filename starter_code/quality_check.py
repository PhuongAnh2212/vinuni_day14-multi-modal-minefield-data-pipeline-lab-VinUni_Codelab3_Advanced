# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    content = str(document_dict.get("content", "")).strip()
    if len(content) < 20:
        return False

    lower_content = content.lower()
    blocked_strings = [
        "null pointer exception",
        "traceback",
        "segmentation fault",
        "fatal error",
    ]
    if any(token in lower_content for token in blocked_strings):
        return False

    source_meta = document_dict.get("source_metadata", {}) or {}
    if (
        source_meta.get("vat_comment_mentions_8_percent")
        and source_meta.get("vat_code_mentions_10_percent")
    ):
        return False

    if "8%" in content and "10%" in content:
        return False

    # Return True if pass, False if fail.
    return True
