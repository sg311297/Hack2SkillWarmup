"""
Monsoon Preparedness & Citizen Assistance Hub

A Streamlit application powered by Gemini AI that provides:
- Personalized monsoon preparedness plans
- Family-specific safety recommendations
- Weather-aware travel advisories
- Emergency checklists
- Real-time crisis management guidance

Author: Crisis Management Team
Created: 2024
"""

import logging
from datetime import datetime

import streamlit as st

import config
from styles import ALL_STYLES
from utils import (
    render_sidebar_panel,
    render_hero_section,
    render_metrics,
    render_result_grid,
    render_checklist,
    render_footer,
    get_api_key_from_secrets,
    initialize_genai_client,
    generate_crisis_plan,
    parse_crisis_plan_response,
    clean_model_field,
)

# ========================================================================
# SETUP & CONFIGURATION
# ========================================================================

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.APP_LAYOUT,
    initial_sidebar_state="expanded",
)

# Apply global styles
st.markdown(ALL_STYLES, unsafe_allow_html=True)

logger.info("Application started")

# ========================================================================
# 1. AUTHENTICATION & API INITIALIZATION
# ========================================================================

api_key = get_api_key_from_secrets()

# Render sidebar with authentication status
render_sidebar_panel(
    title="Secure Gateway" if api_key else "Disaster Management",
    subtitle="API key detected" if api_key else "Enterprise command center",
    icon="🌧️",
    is_authenticated=bool(api_key),
)

# Request API key if not available
if not api_key:
    st.sidebar.markdown("### 🔑 Authentication Setup")
    user_api_key = st.sidebar.text_input(
        label="Enter Gemini API Key to activate:",
        type="password",
        help="Paste your Google Cloud or AI Studio API key here.",
    )
else:
    user_api_key = api_key

# Handle missing API key
if not user_api_key:
    st.warning(config.ERROR_MESSAGES["no_api_key"])
    st.info(config.ERROR_MESSAGES["no_api_key_info"])
    logger.warning("No API key provided - application stopped")
    st.stop()

# Initialize GenAI client
@st.cache_resource(show_spinner=False)
def get_client(validated_key: str):
    """Initialize and cache the GenAI client."""
    try:
        return initialize_genai_client(validated_key)
    except Exception as e:
        logger.error(f"Client initialization failed: {e}")
        st.error(config.ERROR_MESSAGES["api_init_error"].format(error=e))
        st.info(config.ERROR_MESSAGES["api_debug_note"])
        st.stop()


client = get_client(user_api_key)
logger.info("Client initialized successfully")

# ========================================================================
# 2. MAIN DASHBOARD UI
# ========================================================================

st.markdown("<div id='dashboard'></div>", unsafe_allow_html=True)

# Hero section
render_hero_section(
    title="Premium Crisis Response Intelligence",
    subtitle="Deliver high-confidence safety plans, travel advisories, emergency readiness checklists, and real-time family protection guidance powered by Gemini AI.",
    pills=[
        "☁️ Weather Status",
        "🏡 Family Safety",
        "🚨 Emergency Readiness",
        "🤖 AI Assistance",
    ],
)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Metrics display
render_metrics(config.METRICS)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# ========================================================================
# 3. INPUT FORM
# ========================================================================

with st.form(key="monsoon_assistance_form", clear_on_submit=False):
    st.subheader("📋 Citizen Context Profiling", divider="blue")
    
    col_a, col_b = st.columns([1, 1], gap="large")
    
    with col_a:
        location = st.text_input(
            label=config.UI_LABELS["location"],
            value=config.DEFAULT_LOCATION,
            help=config.HELP_TEXTS["location"],
        )
        family_context = st.text_area(
            label=config.UI_LABELS["family_context"],
            placeholder="e.g., 4 family members including an elderly grandparent who uses a wheelchair and a 14-month-old infant.",
            help=config.HELP_TEXTS["family_context"],
        )
    
    with col_b:
        st.subheader("🧭 Scenario Settings", divider="gray")
        st.caption("Fine-tune the advisory output for the right level of urgency.")
        
        weather_severity = st.selectbox(
            label=config.UI_LABELS["severity"],
            options=config.WEATHER_SEVERITY_OPTIONS,
            help=config.HELP_TEXTS["severity"],
        )
        
        language_choice = st.radio(
            label=config.UI_LABELS["language"],
            options=config.LANGUAGE_OPTIONS,
            horizontal=True,
            help=config.HELP_TEXTS["language"],
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    col_button, _ = st.columns([1, 3])
    with col_button:
        submit_btn = st.form_submit_button(label=config.UI_LABELS["generate_button"])

# ========================================================================
# 4. RESPONSE PROCESSING & DISPLAY
# ========================================================================

if submit_btn and family_context and location:
    try:
        # Show loading state
        progress_placeholder = st.empty()
        loading_placeholder = st.empty()
        
        progress_placeholder.progress(20)
        loading_placeholder.markdown(
            """
            <div class='loading-card'>
                <h3>AI Action Plan is being assembled</h3>
                <p style='margin:0 0 8px 0;color:#475569;'>Please hold while Gemini analyzes the regional weather patterns and household risk profile.</p>
                <div class='loading-dots'><span></span><span></span><span></span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Generate crisis plan
        logger.info(f"Generating plan for location: {location}, severity: {weather_severity}")
        raw_response = generate_crisis_plan(
            client=client,
            location=location,
            family_context=family_context,
            weather_severity=weather_severity,
            language_choice=language_choice,
        )
        
        # Parse response
        data = parse_crisis_plan_response(raw_response)
        
        # Clear loading state
        progress_placeholder.progress(100)
        loading_placeholder.empty()
        
        logger.info("Rendering response UI")
        
        # ====== RESULTS SECTION ======
        st.markdown("<div id='preparedness'></div>", unsafe_allow_html=True)
        st.header("🚨 Alert & Preparedness Overview", divider="red")
        st.markdown("**Live advisory:** Actionable insights, safety cards, and AI confidence grouped for high-velocity decision making.")
        
        render_result_grid(data)
        
        # ====== CHECKLIST SECTION ======
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div id='checklist'></div>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div class='section-heading'>
                <div>
                    <h2>📋 Emergency Checklist</h2>
                    <p>Monitor completion progress for your family's critical preparedness steps.</p>
                </div>
                <span class='badge-pill badge-success'>Checklist ready</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        checklist_items = data.get(config.RESPONSE_KEYS["emergency_checklist"], [])
        render_checklist(checklist_items)
        
        # ====== TRAVEL ADVISORY SECTION ======
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div id='travel'></div>", unsafe_allow_html=True)
        
        travel_advisory = clean_model_field(data.get(config.RESPONSE_KEYS["travel_advisory"], "N/A"))
        st.markdown(
            f"""
            <div class='report-card'>
                <h3>📍 Travel Advisory & Safety Controls</h3>
                <p style='margin:0;color:#475569; line-height:1.8;'>{travel_advisory}</p>
                <div style='margin-top:18px; display:flex; flex-wrap:wrap; gap:12px;'>
                    <span class='badge-pill badge-warning'>Flood Routes</span>
                    <span class='badge-pill badge-danger'>Evacuation Ready</span>
                    <span class='badge-pill badge-success'>Sanitation Safe</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # ====== AI GUIDANCE SECTION ======
        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        
        weather_guidance = clean_model_field(data.get(config.RESPONSE_KEYS["weather_guidance"], "N/A"))
        st.markdown(
            f"""
            <div class='report-card'>
                <h3>🧠 AI Guidance Summary</h3>
                <p style='margin:0;color:#475569; line-height:1.8;'>{weather_guidance}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # ====== ACTION BUTTONS & FOOTER ======
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔄 Generate Again with same inputs", key="regen_action"):
                logger.info("User requested plan regeneration")
                st.rerun()
        
        render_footer(datetime.now())
        
        logger.info("Response UI rendered successfully")
    
    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        st.error(config.ERROR_MESSAGES["json_decode_error"])
    
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}", exc_info=True)
        st.error(config.ERROR_MESSAGES["runtime_error"].format(error=e))
        st.info(config.ERROR_MESSAGES["api_debug_note"])

elif submit_btn and not family_context:
    st.warning("⚠️ Please provide family context to generate a personalized plan.")
elif submit_btn and not location:
    st.warning("⚠️ Please provide your location to generate a personalized plan.")
