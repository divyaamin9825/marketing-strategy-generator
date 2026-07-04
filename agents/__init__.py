# agents/__init__.py
# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License")

import os
import json
import google.auth
from google.adk.agents import SequentialAgent
from google.adk.apps import App
from google.adk.agents.callback_context import CallbackContext

# Import the individual agents
from .market_analyst import market_analyst
from .marketing_strategist import marketing_strategist
from .creative_content_creator import creative_content_creator
from .creative_director import creative_director

# Configure environment variables for Vertex AI and GCP
try:
    _, project_id = google.auth.default()
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
except Exception:
    pass

os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

async def init_state(callback_context: CallbackContext) -> None:
    """
    Initializes session state variables. If the user message is a JSON string,
    it parses it to dynamically populate the state keys.
    """
    state = callback_context.state
    
    # Define default values to prevent KeyError
    defaults = {
        "client_name": "Default Client",
        "client_desc": "Default Description",
        "customer_domain": "General Domain",
        "project_description": "General Marketing Campaign",
    }
    
    for key, val in defaults.items():
        if key not in state:
            state[key] = val
            
    # Parse the prompt content if it's a JSON string (used for CLI evals)
    events = callback_context.session.events or []
    for event in events:
        if event.author == "user" and event.content and event.content.parts:
            text = event.content.parts[0].text
            if text and text.strip().startswith("{"):
                try:
                    data = json.loads(text)
                    if "client_name" in data:
                        state["client_name"] = data["client_name"]
                    if "client_desc" in data:
                        state["client_desc"] = data["client_desc"]
                    if "customer_domain" in data:
                        state["customer_domain"] = data["customer_domain"]
                    if "project_overview" in data:
                        state["project_description"] = data["project_overview"]
                    elif "project_description" in data:
                        state["project_description"] = data["project_description"]
                except Exception:
                    pass

# Define the sequential pipeline root agent with before_agent_callback
root_agent = SequentialAgent(
    name="marketing_pipeline",
    sub_agents=[
        market_analyst,
        marketing_strategist,
        creative_content_creator,
        creative_director
    ],
    before_agent_callback=init_state,
)

# Export the app and root_agent
app = App(
    name="agents",
    root_agent=root_agent,
)
