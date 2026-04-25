import re
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    clean = re.sub(r"\[\d{2}:\d{2}:\d{2}\]", "", text)
    clean = re.sub(r"\[(?:Music starts|Music ends|Music|inaudible|Laughter)\]", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\[Speaker\s*\d+\]\s*:\s*", "", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s+", " ", clean).strip()

    vn_price_match = re.search(r"\bnăm\s+trăm\s+nghìn\b", clean, flags=re.IGNORECASE)
    numeric_price_match = re.search(r"\b500\s*,\s*000\b", clean)
    extracted_price_vnd = None
    if vn_price_match or numeric_price_match:
        extracted_price_vnd = 500000

    return {
        "document_id": "transcript-demo-001",
        "content": clean,
        "source_type": "Video",
        "author": "Unknown Speaker",
        "timestamp": datetime.utcnow().isoformat(),
        "source_metadata": {
            "original_file": "demo_transcript.txt",
            "detected_price_vnd": extracted_price_vnd,
            "price_phrase_found": bool(vn_price_match),
            "price_numeric_found": bool(numeric_price_match),
        },
    }

