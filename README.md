# Marketing Strategy Generator

A beginner-friendly Streamlit web application powered by Google ADK 2.0. It uses a team of four cooperative agents to research customer information, formulate marketing strategies, brainstorm campaign ideas, and generate polished ad copies.

## Folder Structure
```
marketing-strategy-generator/
├── README.md
├── app.py                      # Streamlit UI
├── mcp_server.py               # Model Context Protocol (MCP) server
├── requirements.txt            # Python dependencies
├── security.py                 # Input field validation logic
└── agents/                     # ADK 2.0 Agent definitions
    ├── __init__.py             # Pipeline orchestration (SequentialAgent)
    ├── creative_content_creator.py
    ├── creative_director.py
    ├── market_analyst.py
    └── marketing_strategist.py
```

## Agent Team
1. **Market Analyst**: Conducts competitor and audience demographics research.
2. **Marketing Strategist**: Formulates custom digital marketing strategies, channels, and KPIs.
3. **Creative Content Creator**: Develops 5 campaign ideas and writes compelling social media ad copies.
4. **Creative Director**: Oversees, reviews, and compiles the final polished campaign copies.

## Setup & Running the Application

### 1. Prerequisites
Ensure you are in the `marketing-strategy-generator` project directory:
```bash
cd marketing-strategy-generator
```

Verify that Google Cloud Vertex AI credentials and project environment are configured on your system.

### 2. Install Dependencies
Install all package dependencies via `uv` or `pip`:
```bash
uv sync
# OR
pip install -r requirements.txt
```

### 3. Run Streamlit UI
Start the Streamlit application:
```bash
streamlit run app.py
```

### 4. Run MCP Server
You can expose the marketing strategy agent workflow as an MCP tool:
```bash
python mcp_server.py
```

## Running Evaluations

To run evaluation on various test cases (located in `tests/eval/datasets/basic-dataset.json`):
```bash
agents-cli eval run
```
This will run inference over the datasets, grade them using the metrics in `tests/eval/eval_config.yaml`, and generate an interactive HTML report under `artifacts/grade_results/`.
