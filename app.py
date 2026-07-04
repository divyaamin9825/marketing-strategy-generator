# app.py
# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License")

import asyncio
import streamlit as st
from security import validate_inputs
from agents import app as adk_app
from google.adk.runners import InMemoryRunner
from google.genai import types
from pdf_generator import generate_pdf

# Set page configuration for a neat, minimal, and premium look
st.set_page_config(
    page_title="Marketing Strategy Generator",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for rich aesthetics (sleek, modern look)
st.markdown("""
<style>
    .main {
        background-color: #fafafa;
        color: #1e1e1e;
        font-family: 'Outfit', 'Inter', sans-serif;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        color: #333333;
    }
    .stTextArea textarea:focus {
        border-color: #4A90E2;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
    }
    .stButton>button {
        background-color: #1E293B;
        color: #ffffff;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 2rem;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #334155;
        color: #ffffff;
    }
    .copy-container {
        background-color: #0f172a;
        color: #f8fafc !important;
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
        border: 1px solid #1e293b;
        margin-top: 20px;
        font-family: 'Inter', sans-serif;
    }
    .copy-container h1, .copy-container h2, .copy-container h3, .copy-container h4, .copy-container h5, .copy-container h6 {
        color: #f8fafc !important;
        font-weight: 700;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    .copy-container p, .copy-container li, .copy-container span, .copy-container div {
        color: #cbd5e1 !important;
        line-height: 1.6;
    }
    .copy-container strong {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Marketing Strategy Generator")
st.markdown("Generate high-impact campaign ideas and marketing copies tailored to your client using Google ADK 2.0 agents.")

# Text areas for user inputs
client_name = st.text_area("Client name", placeholder="e.g. GreenSprout", height=68)
client_desc = st.text_area("Client description", placeholder="e.g. Organic baby food subscription service", height=80)
customer_domain = st.text_area("Customer Domain", placeholder="e.g. E-commerce & Health Food", height=68)
project_overview = st.text_area("Project overview", placeholder="e.g. Launching a new line of allergen-free plant-based puree pouches", height=100)

async def execute_agent_workflow(inputs: dict):
    """
    Executes the ADK sequential agent pipeline and gathers the results.
    """
    # Create the in-memory runner
    runner = InMemoryRunner(app=adk_app)
    
    # Create a unique session with initial state
    session = await runner.session_service.create_session(
        app_name="agents",
        user_id="streamlit_user",
        state={
            "client_name": inputs["client_name"],
            "client_desc": inputs["client_desc"],
            "customer_domain": inputs["customer_domain"],
            "project_description": inputs["project_overview"],
        }
    )
    
    final_output = ""
    last_author = ""
    
    status_box = st.empty()
    progress_bar = st.progress(0)
    
    # Run the sequential agents in the pipeline
    async for event in runner.run_async(
        user_id="streamlit_user",
        session_id=session.id,
        new_message=types.Content(
            role="user",
            parts=[types.Part.from_text(text="Please research and generate the final marketing copies.")]
        )
    ):
        # Update progress based on which agent is running
        if event.author and event.author != last_author:
            last_author = event.author
            if event.author == "market_analyst":
                status_box.info("🕵️ **Market Analyst** is researching competitors and demographics...")
                progress_bar.progress(25)
            elif event.author == "marketing_strategist":
                status_box.info("📈 **Marketing Strategist** is formulating marketing strategy and KPIs...")
                progress_bar.progress(50)
            elif event.author == "creative_content_creator":
                status_box.info("🎨 **Creative Content Creator** is brainstorming campaign ideas and ad copies...")
                progress_bar.progress(75)
            elif event.author == "creative_director":
                status_box.info("🎬 **Creative Director** is reviewing and finalizing the marketing copies...")
                progress_bar.progress(90)
                
        # Collect final outputs
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    if event.author == "creative_director":
                        final_output += part.text
                        
    # Final step progress
    progress_bar.progress(100)
    status_box.success("✅ Marketing copy generation complete!")
    return final_output

# Trigger on button click
if st.button("upload details"):
    # Construct input dict
    inputs = {
        "client_name": client_name,
        "client_desc": client_desc,
        "customer_domain": customer_domain,
        "project_overview": project_overview,
    }
    
    # Validate using security.py
    is_valid, err_msg = validate_inputs(inputs)
    
    if not is_valid:
        st.error(err_msg)
    else:
        # Run agent execution inside asyncio event loop
        with st.spinner("Initializing Agent Pipeline..."):
            try:
                result = asyncio.run(execute_agent_workflow(inputs))
                
                # Display final output
                st.subheader("📋 Generated Marketing Campaigns & Copies")
                st.markdown(f'<div class="copy-container">{result}</div>', unsafe_allow_html=True)
                
                # Generate PDF and offer download button
                with st.spinner("Generating PDF..."):
                    pdf_bytes = generate_pdf(inputs["client_name"], result)
                    
                st.download_button(
                    label="📥 Download Strategy & Copies as PDF",
                    data=pdf_bytes,
                    file_name=f"{inputs['client_name'].lower().replace(' ', '_')}_marketing_strategy.pdf",
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"An error occurred during execution: {e}")
