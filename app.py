import json
import uuid
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

from result_enhancer import (
    ensure_output_dir,
    build_competitor_table,
    save_competitor_table_csv,
    build_markdown_report,
    save_markdown_report,
    build_insight_cards,
    save_insight_cards,
)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "outputs"

st.set_page_config(
    page_title="Industry Intelligence Agent",
    layout="wide"
)


def call_dify_chatflow(user_query: str, analysis_depth: str, focus_area: str, mode: str) -> str:
    api_key = st.secrets["DIFY_API_KEY"]
    base_url = st.secrets["DIFY_BASE_URL"]

    url = f"{base_url}/chat-messages"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": {
            "analysis_depth": analysis_depth,
            "focus_area": focus_area,
            "mode": mode
        },
        "query": user_query,
        "response_mode": "streaming",
        "user": str(uuid.uuid4())
    }

    resp = requests.post(
        url,
        headers=headers,
        json=payload,
        stream=True,
        timeout=180
    )
    resp.raise_for_status()

    final_answer = ""

    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        if line.startswith("data: "):
            content = line[6:]
            if content == "[DONE]":
                break
            try:
                event = json.loads(content)
                if event.get("event") == "message" and "answer" in event:
                    final_answer += event["answer"]
            except Exception:
                continue

    return final_answer


def parse_dify_json_response(raw_text: str) -> dict:
    cleaned = raw_text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "", 1).strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```", "", 1).strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()

    return json.loads(cleaned)


st.title("Industry Intelligence Agent")
st.caption("Analyze any industry, compare competitors, identify market signals, and get practical entry advice.")

with st.sidebar:
    st.header("Analysis Setup")

    user_query = st.text_area(
        "Research Question",
        value="Analyze China's coffee chain market and evaluate whether there is still room for new entrants.",
        height=120
    )

    analysis_depth = st.text_input(
        "Analysis Depth (standard or deep)",
        value="deep"
    )

    focus_area = st.text_input(
        "Focus Area (full / market / competitor / strategy)",
        value="strategy"
    )

    mode = st.text_input(
        "Analysis Mode (full_report / competitor_snapshot / trend_insight / entry_advisor)",
        value="entry_advisor"
    )

    run_button = st.button("Generate Analysis")

if run_button:
    try:
        raw_response = call_dify_chatflow(
            user_query=user_query,
            analysis_depth=analysis_depth,
            focus_area=focus_area,
            mode=mode
        )

        data = parse_dify_json_response(raw_response)

        ensure_output_dir()

        competitor_rows = build_competitor_table(data)
        save_competitor_table_csv(competitor_rows)

        report_md = build_markdown_report(data, competitor_rows)
        save_markdown_report(report_md)

        cards = build_insight_cards(data)
        save_insight_cards(cards)

        table_df = pd.DataFrame(competitor_rows)

        st.success("Your industry analysis is ready.")

        st.subheader("Analysis Request")
        st.markdown(f"**Question:** {user_query}")
        st.markdown(f"**Depth:** {analysis_depth}")
        st.markdown(f"**Focus:** {focus_area}")
        st.markdown(f"**Mode:** {mode}")

        tab1, tab2, tab3 = st.tabs(["Industry Report", "Competitor Snapshot", "Insight Cards"])

        with tab1:
            st.subheader("Final Report")
            st.markdown(data.get("final_report_markdown", report_md))

        with tab2:
            st.subheader("Competitor Comparison")
            if not table_df.empty:
                st.dataframe(table_df, use_container_width=True)
            else:
                st.warning("No competitor table data available.")

        with tab3:
            st.subheader("Insight Cards")
            if cards:
                cols = st.columns(2)
                for i, card in enumerate(cards):
                    with cols[i % 2]:
                        with st.container(border=True):
                            st.markdown(f"### {card.get('title', 'Untitled')}")
                            items = card.get("items", [])
                            for item in items:
                                st.markdown(f"- {item}")
            else:
                st.warning("No insight cards available.")

        with st.expander("Raw JSON Output"):
            st.json(data)

    except Exception as e:
        st.error(f"Failed to call Dify: {e}")

else:
    st.info("Enter an industry question on the left and click 'Generate Analysis' to view the report, competitor snapshot, and insight cards.")