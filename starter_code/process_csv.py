import pandas as pd
import re
from datetime import datetime

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Process sales records, handling type traps and duplicates.

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    df = df.drop_duplicates(subset=["id"], keep="first").copy()

    def _price_to_float(value):
        if pd.isna(value):
            return None
        text = str(value).strip().lower()
        if text in {"n/a", "null", "none", "liên hệ", "lien he", ""}:
            return None
        word_map = {"five dollars": 5.0}
        if text in word_map:
            return word_map[text]
        cleaned = re.sub(r"[^0-9.\-]", "", text)
        try:
            return float(cleaned) if cleaned else None
        except ValueError:
            return None

    def _normalize_date(value):
        if pd.isna(value):
            return None
        parsed = pd.to_datetime(value, errors="coerce", dayfirst=True)
        if pd.isna(parsed):
            parsed = pd.to_datetime(value, errors="coerce", dayfirst=False)
        if pd.isna(parsed):
            return None
        return parsed.strftime("%Y-%m-%d")

    df["price_clean"] = df["price"].apply(_price_to_float)
    df["date_clean"] = df["date_of_sale"].apply(_normalize_date)

    documents = []
    for _, row in df.iterrows():
        row_dict = row.to_dict()
        doc_id = f"csv-{int(row_dict['id'])}"
        content = (
            f"Sale record {int(row_dict['id'])}: {row_dict['product_name']} "
            f"in category {row_dict['category']} sold on {row_dict['date_clean']}."
        )
        documents.append(
            {
                "document_id": doc_id,
                "content": content,
                "source_type": "CSV",
                "author": "Sales System",
                "timestamp": datetime.utcnow().isoformat(),
                "source_metadata": {
                    "original_file": "sales_records.csv",
                    "price_raw": row_dict.get("price"),
                    "price_clean": row_dict.get("price_clean"),
                    "currency": row_dict.get("currency"),
                    "date_raw": row_dict.get("date_of_sale"),
                    "date_normalized": row_dict.get("date_clean"),
                    "seller_id": row_dict.get("seller_id"),
                    "stock_quantity": row_dict.get("stock_quantity"),
                },
            }
        )

    return documents

