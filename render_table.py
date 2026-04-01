import csv
from pathlib import Path
from typing import List, Dict

INPUT_FILE = Path("outputs/competitor_table.csv")
OUTPUT_FILE = Path("outputs/competitor_table.html")


def load_table(file_path: Path) -> List[Dict[str, str]]:
    rows = []
    with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def build_table_rows(rows: List[Dict[str, str]]) -> str:
    html_rows = ""
    for row in rows:
        company = row.get("company_name", "")
        positioning = row.get("positioning", "")
        risk = row.get("risk", "")
        html_rows += f"""
        <tr>
            <td>{company}</td>
            <td>{positioning}</td>
            <td>{risk}</td>
        </tr>
        """
    return html_rows


def build_page(rows: List[Dict[str, str]]) -> str:
    table_rows = build_table_rows(rows)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Competitor Comparison Table</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            margin: 0;
            padding: 40px;
            color: #1f2937;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            font-size: 32px;
            margin-bottom: 24px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
        }}
        th, td {{
            text-align: left;
            padding: 16px;
            vertical-align: top;
            border-bottom: 1px solid #e5e7eb;
            line-height: 1.5;
        }}
        th {{
            background: #eef2ff;
            font-size: 16px;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Competitor Comparison Table</h1>
        <table>
            <thead>
                <tr>
                    <th>Company</th>
                    <th>Positioning</th>
                    <th>Risk</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
</body>
</html>
"""


def main() -> None:
    rows = load_table(INPUT_FILE)
    html = build_page(rows)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done. Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()