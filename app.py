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

# Custom CSS for rich aesthetics (premium dark mode with glassmorphic cards and gradients)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global App Container background & font overrides */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #090d16 0%, #111827 50%, #030712 100%) !important;
        color: #f3f4f6 !important;
        font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Input Fields styling override */
    div[data-baseweb="input"], div[data-baseweb="textarea"] {
        background-color: rgba(17, 24, 39, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #f3f4f6 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.25) !important;
        background-color: rgba(17, 24, 39, 0.9) !important;
    }
    
    input, textarea {
        color: #f3f4f6 !important;
        font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif !important;
        font-size: 0.95rem !important;
    }

    /* Labels styling */
    label[data-testid="stWidgetLabel"] p {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #9ca3af !important;
        letter-spacing: 0.025em;
        margin-bottom: 6px !important;
        text-transform: uppercase;
    }

    /* Primary CTA Button (Upload Details) styling */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.75rem 2rem !important;
        border: none !important;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
        margin-top: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.5) !important;
        color: #ffffff !important;
    }

    .stButton>button:active {
        transform: translateY(0);
    }

    /* Download PDF Button styling */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.75rem 2rem !important;
        border: none !important;
        box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
        width: 100%;
        margin-top: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(16, 185, 129, 0.5) !important;
        color: #ffffff !important;
    }
    
    /* Styled container with borders (cards) */
    div[data-testid="stElementContainer"] > div[style*="border"] {
        background-color: rgba(17, 24, 39, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 1.75rem !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25) !important;
        backdrop-filter: blur(16px) !important;
        margin-bottom: 1.5rem !important;
    }

    /* Styled notification boxes */
    div[data-testid="stNotification"] {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #cbd5e1 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Spinner override styling */
    div[data-testid="stSpinner"] > div {
        border-color: #818cf8 transparent transparent transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom Header / Title Section
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem; margin-top: 1.5rem;">
    <div style="display: inline-block; background: linear-gradient(90deg, rgba(99, 102, 241, 0.2), rgba(192, 132, 252, 0.2)); border: 1px solid rgba(129, 140, 248, 0.3); border-radius: 20px; padding: 4px 16px; margin-bottom: 1rem;">
        <span style="color: #c084fc; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">
            ✨ Powered by Google ADK 2.0
        </span>
    </div>
    <h1 style="background: linear-gradient(90deg, #818cf8 0%, #c084fc 50%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; letter-spacing: -0.03em; margin: 0;">
        Marketing Strategy Generator
    </h1>
    <p style="color: #94a3b8; font-size: 1.1rem; margin-top: 0.75rem; max-width: 600px; margin-left: auto; margin-right: auto; line-height: 1.5;">
        Generate high-impact campaign ideas and custom marketing copy using a collaborative team of AI agents.
    </p>
</div>
""", unsafe_allow_html=True)

# Campaign Configuration Form within a glassmorphic container card
with st.container(border=True):
    st.markdown("<h3 style='margin-top:0; color:#818cf8; font-size: 1.25rem; font-weight: 700; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem; margin-bottom: 1.25rem;'>📋 Campaign Configuration</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Client Name", placeholder="e.g. GreenSprout")
        customer_domain = st.text_input("Customer Domain", placeholder="e.g. E-commerce & Health Food")
    with col2:
        client_desc = st.text_area("Client Description", placeholder="e.g. Organic baby food subscription service", height=95)
    
    project_overview = st.text_area("Project Overview", placeholder="e.g. Launching a new line of allergen-free plant-based puree pouches", height=100)

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
if st.button("Upload Details"):
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
                with st.container(border=True):
                    st.markdown("<h3 style='margin-top:0; color:#818cf8; font-size: 1.25rem; font-weight: 700; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.5rem; margin-bottom: 1.25rem;'>📋 Generated Marketing Campaigns & Copies</h3>", unsafe_allow_html=True)
                    st.markdown(result)
                
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
