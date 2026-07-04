# mcp_server.py
# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License")

import asyncio
from mcp.server.fastmcp import FastMCP
from security import validate_inputs
from agents import app as adk_app
from google.adk.runners import InMemoryRunner
from google.genai import types

# Create a FastMCP server named marketing-strategy-generator
mcp = FastMCP("marketing-strategy-generator")

@mcp.tool()
async def generate_marketing_strategy_and_copies(
    client_name: str,
    client_desc: str,
    customer_domain: str,
    project_overview: str
) -> str:
    """
    Generates structured marketing strategies and 5 social media campaign ad copies.
    
    Args:
        client_name: The name of the client company.
        client_desc: A brief description of the client's business model and products.
        customer_domain: The primary market or industry domain of the customer.
        project_overview: The project or campaign overview we are working on.
    """
    inputs = {
        "client_name": client_name,
        "client_desc": client_desc,
        "customer_domain": customer_domain,
        "project_overview": project_overview,
    }
    
    # Run security.py validation
    is_valid, err_msg = validate_inputs(inputs)
    if not is_valid:
        return f"Validation Failure: {err_msg}"
        
    # Setup the ADK Runner
    runner = InMemoryRunner(app=adk_app)
    
    # Create a session with initial state
    session = await runner.session_service.create_session(
        app_name="agents",
        user_id="mcp_user",
        state={
            "client_name": client_name,
            "client_desc": client_desc,
            "customer_domain": customer_domain,
            "project_description": project_overview,
        }
    )
    
    final_output = ""
    
    # Run the sequential agents in the pipeline
    async for event in runner.run_async(
        user_id="mcp_user",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part.from_text(text="Generate the marketing strategies and copies.")]
        )
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text and event.author == "creative_director":
                    final_output += part.text
                    
    return final_output

if __name__ == "__main__":
    mcp.run()
