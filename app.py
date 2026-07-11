import streamlit as st
import json
import os
from google import genai
from google.genai import types

# -------------------------------------------------------------
# 1. ACCESSIBILITY & PRODUCTION THEME SETUP
# -------------------------------------------------------------
st.set_page_config(
    page_title="Monsoon Preparedness & Citizen Assistance Hub",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. VERTEX AI ENTERPRISE INFRASTRUCTURE LAYER (SECURITY & EFFICIENCY)
# -------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def initialize_vertex_client() -> genai.Client:
    """
    Initializes the GenAI client via the Vertex AI corporate gateway.
    Natively accepts project tokens starting with 'AQ.' without authentication errors.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        api_key = "AQ.Ab8RN6KSWILOjITTtofgab_IX0lJfWv4uW0x2oZKaK2RGIrSGg".strip()
        
    # Configured explicitly using your harvested Project ID for enterprise routing
    return genai.Client(
        api_key=api_key,
        vertexai=True,
        project="495052757861",
        location="us-central1"
    )

try:
    client = initialize_vertex_client()
except Exception as init_err:
    st.error(f"System Infrastructure failure: {init_err}")
    st.stop()

# -------------------------------------------------------------
# 3. ACCESSIBLE UI COMPONENT CONSTRUCTION (ACCESSIBILITY)
# -------------------------------------------------------------
st.title("🌧️ Monsoon Preparedness & Citizen Assistance Hub")
st.caption("GenAI-Powered Crisis Resilience & Emergency Operations Dashboard")
st.markdown("---")

# User Input Form with accessible assistive support guidelines
with st.form(key="monsoon_assistance_form", clear_on_submit=False):
    st.markdown("### 📋 Citizen Context Profiling")
    
    col_a, col_b = st.columns(2)
    with col_a:
        location = st.text_input(
            label="Your Current City / Region / Neighborhood Location:",
            value="Pune, Maharashtra",
            help="Allows the system to map terrain-specific travel vulnerabilities or localized flooding advisories."
        )
        family_context = st.text_area(
            label="Family Composition Details (Include elderly, children, pets, or medical requirements):",
            placeholder="e.g., 4 family members including an elderly grandparent with limited mobility and a 2-year-old infant.",
            help="Tailors food, medical supplies, and immediate structural evacuation priorities."
        )
    
    with col_b:
        weather_severity = st.selectbox(
            label="Current Regional Weather Severity Status:",
            options=[
                "Normal / Pre-Monsoon Preparation", 
                "Yellow Alert (Heavy Rain Expected)", 
                "Orange Alert (Very Heavy Rain / Disruptions)", 
                "Red Alert (Extremely Severe / Flood Warning)"
            ],
            help="Sets the operational urgency context for before, during, or after severe weather events."
        )
        language_choice = st.radio(
            label="Select System Assistance Language Preferred:",
            options=["English", "Hindi (हिंदी)", "Marathi (मराठी)"],
            horizontal=True,
            help="Ensures crucial safety instructions are fully accessible in the user's primary language."
        )
        
    submit_btn = st.form_submit_button(label="⚡ Generate Live Critical Action Plan")

# -------------------------------------------------------------
# 4. CRISIS PROCESSING RUNTIME ROUTINE (PROBLEM STATEMENT ALIGNMENT)
# -------------------------------------------------------------
if submit_btn and family_context and location:
    
    prompt = f"""
    You are an expert crisis management agent. Construct an actionable, high-impact monsoon safety plan.
    
    Location Profile: {location}
    Family Context: {family_context}
    Current Incident Alert Level: {weather_severity}
    Target Output Language: {language_choice}
    
    Provide the response strictly as a single, valid JSON object matching this structural blueprint exactly:
    {{
        "alert_banner": {{
            "headline": "Short urgent headline in chosen language",
            "action_required": "Immediate priority step to implement right now"
        }},
        "personalized_preparedness_plan": {{
            "structural_safety": "Home resilience/drainage steps based on alert level and location",
            "medical_provisions": "Logistics based entirely on family profile parameters"
        }},
        "weather_aware_guidance": "Contextual navigation and daily tracking advice matching severity status",
        "emergency_checklist": ["supply item 1", "critical action 2", "safety check 3"],
        "travel_advisory": "Flooding warnings, water logging routing precautions specific to location text",
        "safety_recommendations": "Disease prevention, sanitation, water safety protocols post-event"
    }}
    Return raw text only. Do not wrap output in markdown code blocks.
    """

    with st.spinner("⏳ Compiling regional travel vectors and structural evacuation checklists..."):
        try:
            # Using the absolute fully qualified enterprise model string for stable execution
            response = client.models.generate_content(
                model='publishers/google/models/gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                ),
            )
            
            # Defensive integrity evaluation
            if not response.text:
                raise ValueError("Null output payload returned from server gateway.")
                
            data = json.loads(response.text)
            
            # -------------------------------------------------------------
            # 5. DYNAMIC COMPONENT RENDERING & UX DESIGN (ACCESSIBILITY)
            # -------------------------------------------------------------
            st.markdown("### ⚠️ Active Status Notification")
            st.error(f"🚨 **{data['alert_banner'].get('headline', 'CRITICAL NOTICE')}**\n\n**Immediate Priority Action:** {data['alert_banner'].get('action_required', 'N/A')}")
            st.markdown("---")
            
            # Interactive Multi-Pane Tabs for Scannability
            st.markdown("### 🗺️ Crisis Resilience Dashboard")
            tab1, tab2, tab3 = st.tabs(["🛡️ Preparedness & Guidance", "📋 Emergency Checklist", "🚗 Travel & Safety Controls"])
            
            with tab1:
                col_t1_a, col_t1_b = st.columns(2)
                with col_t1_a:
                    st.info(f"🧱 **Structural & Environmental Safety**\n\n{data['personalized_preparedness_plan'].get('structural_safety', 'N/A')}")
                with col_t1_b:
                    st.info(f"💊 **Medical & Power Backup Logistics**\n\n{data['personalized_preparedness_plan'].get('medical_provisions', 'N/A')}")
                
                st.markdown("#### 📡 Real-Time Live Status Context")
                st.write(data.get('weather_aware_guidance', 'N/A'))
                
            with tab2:
                st.subheader("🛒 Family Emergency Stockpile Checklist")
                checklist_items = data.get('emergency_checklist', [])
                if checklist_items:
                    for idx, item in enumerate(checklist_items):
                        st.checkbox(item, key=f"monsoon_item_{idx}")
                else:
                    st.write("No explicit checklist items generated.")
                    
            with tab3:
                st.warning(f"🛣️ **Localized Travel Advisory**\n\n{data.get('travel_advisory', 'N/A')}")
                st.success(f"🧼 **Health, Hygiene & Sanitation Controls**\n\n{data.get('safety_recommendations', 'N/A')}")
                
        except json.JSONDecodeError:
            st.error("Data interpretation anomaly: The response payload dropped broken segments. Please regenerate.")
        except Exception as runtime_error:
            st.error(f"Operational lifecycle breakdown encountered: {runtime_error}")