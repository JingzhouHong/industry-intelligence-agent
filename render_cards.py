import json
from pathlib import Path
from typing import Any, Dict, List

INPUT_FILE = Path("outputs/insight_cards.json")
OUTPUT_FILE = Path("outputs/insight_cards.html")


def load_cards(file_path: Path) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_card_html(card: Dict[str, Any]) -> str:
    title = card.get("title", "Untitled")
    items = card.get("items", [])

    list_items = ""
    for item in items:
        list_items += f"<li>{item}</li>\n"

    return f"""
    <div class="card">
        <h2>{title}</h2>
        <ul>
            {list_items}
        </ul>
    </div>
    """


def build_page(cards: List[Dict[str, Any]]) -> str:
    cards_html = "\n".join(build_card_html(card) for card in cards)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Industry Insight Cards</title>
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
            margin-bottom: 30px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
        }}
        .card h2 {{
            font-size: 20px;
            margin-top: 0;
            margin-bottom: 16px;
        }}
        .card ul {{
            padding-left: 20px;
            margin: 0;
        }}
        .card li {{
            margin-bottom: 10px;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Industry Insight Cards</h1>
        <div class="grid">
            {cards_html}
        </div>
    </div>
</body>
</html>
"""


def main() -> None:
    cards = load_cards(INPUT_FILE)
    html = build_page(cards)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done. Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()