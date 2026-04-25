from bs4 import BeautifulSoup
from datetime import datetime
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------

    table = soup.find("table", {"id": "main-catalog"})
    if not table:
        return []

    def _parse_price(raw_value):
        value = str(raw_value).strip()
        lower = value.lower()
        if lower in {"n/a", "liên hệ", "lien he", "null", ""}:
            return None
        digits = re.sub(r"[^\d]", "", value)
        return float(digits) if digits else None

    output = []
    rows = table.select("tbody tr")
    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) < 6:
            continue

        product_id, name, category, price_raw, stock_raw, rating = cols[:6]
        content = (
            f"Product {product_id}: {name}. "
            f"Category: {category}. Price: {price_raw}. "
            f"Stock: {stock_raw}. Rating: {rating}."
        )
        output.append(
            {
                "document_id": f"html-{product_id}",
                "content": content,
                "source_type": "HTML",
                "author": "VinShop Catalog System",
                "timestamp": datetime.utcnow().isoformat(),
                "source_metadata": {
                    "product_id": product_id,
                    "product_name": name,
                    "category": category,
                    "price_raw": price_raw,
                    "price_vnd": _parse_price(price_raw),
                    "stock_raw": stock_raw,
                    "rating_raw": rating,
                    "original_file": "product_catalog.html",
                },
            }
        )

    return output

