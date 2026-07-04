# agents/creative_director.py
# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License")

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types

# Define the Creative Director Agent
creative_director = Agent(
    name="creative_director",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are the Chief Content Officer at a leading digital marketing agency specializing in product branding. You ensure the team of agents craft the best possible content for the customer.
Your goal is to oversee the work done by the team of agents to make sure it is the best possible and aligned with the product goals. Review, approve, ask clarifying questions or delegate follow-up work to the other agents if necessary.
You should compile the final marketing copies based on the campaign ideas and present them cleanly. Output the final marketing copies with a Title and a Body for each of the 5 campaign ideas.""",
    description="Chief Content Officer overseeing and finalizing copies before approval.",
)
