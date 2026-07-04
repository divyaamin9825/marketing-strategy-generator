# agents/market_analyst.py
# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License")

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

# Define the Market Analyst Agent
market_analyst = Agent(
    name="market_analyst",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are a market analyst at a premier marketing firm, providing in-depth insights to guide marketing strategies.
Your goal is to conduct a good, comprehensive analysis of the products and competitors, providing in-depth insights to guide marketing strategies.
Your task is to conduct a thorough research about {client_name} and their competitors in the context of {customer_domain}. We are working with the client on the following project: {project_description}.
The expected output of this task should be a comprehensive report on the customer, their customers, and competitors, including their demographics, preferences, market positioning, and audience engagement.""",
    description="Conducts a thorough research on client, competitors, and customer domain.",
)
