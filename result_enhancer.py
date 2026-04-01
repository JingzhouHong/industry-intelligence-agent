import json
import csv
from pathlib import Path
from typing import Any, Dict, List


INPUT_FILE = "sample_output.json"
OUTPUT_DIR = Path("outputs")


def load_data(file_path: str) -> Dict[str, Any]:
    """Load structured workflow output from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_output_dir() -> None:
    """Create output directory if it does not exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_competitor_table(data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Build a competitor comparison table from competitor-related fields.
    This first version assumes aligned arrays by index.
    """
    names = data.get("competitor_names", [])
    positions = data.get("positioning_summary", [])
    risks = data.get("risk_summary", [])

    rows: List[Dict[str, str]] = []
    max_len = max(len(names), len(positions), len(risks), 0)

    for i in range(max_len):
        rows.append({
            "company_name": names[i] if i < len(names) else "",
            "positioning": positions[i] if i < len(positions) else "",
            "risk": risks[i] if i < len(risks) else ""
        })

    return rows


def save_competitor_table_csv(rows: List[Dict[str, str]]) -> Path:
    """Save competitor comparison table as CSV."""
    output_file = OUTPUT_DIR / "competitor_table.csv"
    with open(output_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["company_name", "positioning", "risk"]
        )
        writer.writeheader()
        writer.writerows(rows)
    return output_file


def format_list(items: List[str]) -> str:
    """Convert a list of strings into markdown bullet points."""
    if not items:
        return "- N/A"
    return "\n".join(f"- {item}" for item in items)


def build_markdown_report(data: Dict[str, Any], competitor_rows: List[Dict[str, str]]) -> str:
    """Build a cleaner markdown report from workflow outputs."""
    topic = data.get("research_topic", "N/A")
    goal = data.get("research_goal", "N/A")
    dimensions = format_list(data.get("research_dimensions", []))
    target_companies = format_list(data.get("target_companies", []))
    key_insights = format_list(data.get("key_insights", []))
    opportunity_areas = format_list(data.get("opportunity_areas", []))
    suggested_strategies = format_list(data.get("suggested_strategies", []))
    key_risks = format_list(data.get("key_risks", []))
    avoid_actions = format_list(data.get("avoid_actions", []))
    entry_recommendation = data.get("entry_recommendation", "N/A")

    # Build markdown table
    if competitor_rows:
        table_lines = [
            "| Company | Positioning | Risk |",
            "|---|---|---|"
        ]
        for row in competitor_rows:
            company = row["company_name"].replace("|", "/")
            positioning = row["positioning"].replace("|", "/")
            risk = row["risk"].replace("|", "/")
            table_lines.append(f"| {company} | {positioning} | {risk} |")
        competitor_table_md = "\n".join(table_lines)
    else:
        competitor_table_md = "No competitor data available."

    report = f"""# Industry Intelligence Report

## 1. Research Topic
{topic}

## 2. Research Goal
{goal}

## 3. Research Dimensions
{dimensions}

## 4. Target Companies
{target_companies}

## 5. Competitor Snapshot
{competitor_table_md}

## 6. Key Insights
{key_insights}

## 7. Opportunity Areas
{opportunity_areas}

## 8. Entry Recommendation
{entry_recommendation}

## 9. Suggested Strategies
{suggested_strategies}

## 10. Key Risks
{key_risks}

## 11. Avoid Actions
{avoid_actions}
"""
    return report


def save_markdown_report(report: str) -> Path:
    """Save markdown report to file."""
    output_file = OUTPUT_DIR / "industry_report.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    return output_file


def build_insight_cards(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Build a simple card-style JSON output for demo and portfolio usage."""
    cards = [
        {
            "card_type": "key_insights",
            "title": "Key Insights",
            "items": data.get("key_insights", [])
        },
        {
            "card_type": "opportunity_areas",
            "title": "Opportunity Areas",
            "items": data.get("opportunity_areas", [])
        },
        {
            "card_type": "entry_recommendation",
            "title": "Entry Recommendation",
            "items": [data.get("entry_recommendation", "N/A")]
        },
        {
            "card_type": "suggested_strategies",
            "title": "Suggested Strategies",
            "items": data.get("suggested_strategies", [])
        },
        {
            "card_type": "key_risks",
            "title": "Key Risks",
            "items": data.get("key_risks", [])
        }
    ]
    return cards


def save_insight_cards(cards: List[Dict[str, Any]]) -> Path:
    """Save card-style results as JSON."""
    output_file = OUTPUT_DIR / "insight_cards.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)
    return output_file


def main() -> None:
    """Run the result enhancement pipeline."""
    ensure_output_dir()
    data = load_data(INPUT_FILE)

    competitor_rows = build_competitor_table(data)
    competitor_csv = save_competitor_table_csv(competitor_rows)

    report_md = build_markdown_report(data, competitor_rows)
    markdown_file = save_markdown_report(report_md)

    cards = build_insight_cards(data)
    cards_file = save_insight_cards(cards)

    print("Done. Generated files:")
    print(f"- {competitor_csv}")
    print(f"- {markdown_file}")
    print(f"- {cards_file}")


if __name__ == "__main__":
    main()