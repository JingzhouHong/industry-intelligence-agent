# Industry Intelligence Agent

An online industry research product that transforms user questions into structured industry reports, competitor snapshots, insight cards, and market entry recommendations.

## Overview

Industry Intelligence Agent is a lightweight AI product for industry analysis and strategic research.

Users can enter any industry-related question, such as:

- Is there still room for new entrants in China's industrial robot market?
- What is the competitive landscape of AI companion products in China?
- How should a new brand enter China's pet food market?

The system then generates:

- an industry report
- a competitor snapshot
- insight cards
- market entry advice

## Demo

- Live App: [https://industry-intelligence-agent-eyfy98th2nfnjdghbwvppv.streamlit.app/]

## What the product does

This product is designed to help users quickly turn an industry question into structured analysis.

Main outputs include:

1. **Industry Report**  
   A readable markdown-style report covering topic, goal, dimensions, insights, opportunities, risks, and recommendations.

2. **Competitor Snapshot**  
   A structured comparison of major players, including positioning and key risks.

3. **Insight Cards**  
   A card-based summary of key insights, opportunity areas, strategies, and risks.

## System Architecture

The project has three layers:

### 1. Dify Agent Workflow Layer
Built with Dify Cloud.

Main responsibilities:

- task understanding
- research planning
- competitor analysis
- insight generation
- decision support
- API output packaging

This layer handles the core agent workflow and returns a structured JSON response.

### 2. Python Result Enhancement Layer
Built with Python.

Main responsibilities:

- generate markdown report
- build competitor comparison table
- generate insight cards
- save structured outputs for rendering

This layer turns raw workflow outputs into cleaner user-facing deliverables.

### 3. Streamlit Product Interface
Built with Streamlit.

Main responsibilities:

- collect user input
- call Dify API
- trigger Python enhancement logic
- display the final report, table, and cards in one interface

## Workflow Logic

The system follows a multi-step industry analysis workflow:

1. **Task Understanding**  
   Understand the user’s question, industry, and research goal.

2. **Research Planning**  
   Define research dimensions and target companies.

3. **Competitor Analysis**  
   Summarize competitor positioning and major risks.

4. **Insight Generation**  
   Identify key signals, opportunity areas, and market implications.

5. **Decision Support**  
   Generate market entry recommendations, strategies, risks, and avoid-actions.

6. **API Output Packager**  
   Convert all workflow outputs into structured JSON for frontend rendering.

## Supported Modes

The product supports multiple analysis modes:

- `full_report`
- `competitor_snapshot`
- `trend_insight`
- `entry_advisor`

These modes allow the same workflow to serve different analytical needs.

## Tech Stack

- **Dify Cloud** — agent workflow orchestration
- **Qwen / Tongyi model API** — LLM backend
- **Python** — result enhancement
- **Streamlit** — frontend interface
- **GitHub** — code hosting
- **Streamlit Community Cloud** — deployment

## Project Structure

```text
industry-intelligence-agent/
├── app.py
├── result_enhancer.py
├── render_cards.py
├── render_table.py
├── requirements.txt
├── sample_output.json
├── outputs/
└── .gitignore