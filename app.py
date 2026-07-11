import streamlit as st
import json
import os
from datetime import datetime
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
# 1.1 GLOBAL UI STYLING
# -------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Nunito:wght@400;600;700&display=swap');
    :root {
        color-scheme: light;
        font-family: 'Inter', 'Nunito', sans-serif;
        background: #f8fafc;
    }
    html, body {
        background: #f8fafc;
    }
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #eef4fb 100%);
        color: #0f172a;
    }
    .hero-panel,
    .glass-card,
    .sidebar-card,
    .result-card,
    .loading-card,
    .report-card {
        border-radius: 22px;
        background: rgba(255,255,255,0.86);
        box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
        border: 1px solid rgba(255,255,255,0.72);
        backdrop-filter: blur(18px);
        padding: 28px;
    }
    .hero-panel {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(37,99,235,0.95), rgba(20,184,166,0.9));
        color: #ffffff;
        border: none;
    }
    .hero-panel::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top left, rgba(255,255,255,0.22), transparent 24%),
                    radial-gradient(circle at bottom right, rgba(255,255,255,0.16), transparent 18%);
        pointer-events: none;
    }
    .hero-content {
        position: relative;
        z-index: 1;
    }
    .hero-title {
        font-size: clamp(2.55rem, 2.35vw, 3.75rem);
        line-height: 1.02;
        margin: 0;
        letter-spacing: -0.05em;
        font-weight: 800;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.92;
        max-width: 760px;
        margin-top: 14px;
        line-height: 1.75;
    }
    .hero-pill-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 16px;
        margin-top: 28px;
    }
    .hero-pill {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px 18px;
        border-radius: 18px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.18);
        color: #ffffff;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .hero-pill span {
        font-size: 1.35rem;
    }
    .metric-card {
        border-radius: 22px;
        border: 1px solid rgba(15,23,42,0.08);
        padding: 24px;
        background: #ffffff;
        box-shadow: 0 18px 40px rgba(15,23,42,0.06);
        min-height: 140px;
    }
    .metric-card h4 {
        margin: 0 0 12px;
        font-size: 0.95rem;
        color: #475569;
        font-weight: 600;
    }
    .metric-card p {
        margin: 0;
        font-size: 1.85rem;
        font-weight: 700;
        color: #0f172a;
    }
    .sidebar-panel {
        border-radius: 24px;
        padding: 22px;
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(15,23,42,0.06);
        box-shadow: 0 24px 50px rgba(15,23,42,0.08);
        margin-bottom: 18px;
    }
    .sidebar-brand {
        display: flex;
        gap: 14px;
        align-items: center;
        margin-bottom: 20px;
    }
    .sidebar-brand .brand-icon {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 14px;
        background: linear-gradient(135deg, #2563eb, #14b8a6);
        color: white;
        font-size: 1.15rem;
    }
    .sidebar-brand h2 {
        margin: 0;
        font-size: 1.05rem;
        line-height: 1.2;
        color: #0f172a;
    }
    .sidebar-link {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
        color: #0f172a;
        padding: 12px 14px;
        border-radius: 16px;
        margin-bottom: 8px;
        transition: all 180ms ease;
        border: 1px solid transparent;
        font-size: 0.98rem;
        background: rgba(15,23,42,0.02);
    }
    .sidebar-link:hover {
        transform: translateX(4px);
        border-color: rgba(37,99,235,0.18);
        background: rgba(37,99,235,0.06);
    }
    .sidebar-divider {
        height: 1px;
        background: rgba(15,23,42,0.08);
        margin: 18px 0;
    }
    .glass-card h3,
    .result-card h3,
    .loading-card h3 {
        margin-top: 0;
        margin-bottom: 12px;
        font-size: 1.25rem;
    }
    .result-grid {
        display: grid;
        gap: 20px;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    }
    .result-card {
        position: relative;
        overflow: hidden;
    }
    .result-card .card-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        border-radius: 14px;
        margin-bottom: 14px;
        font-size: 1.25rem;
    }
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    .badge-success { background: rgba(34,197,94,0.12); color: #166534; }
    .badge-warning { background: rgba(245,158,11,0.12); color: #92400e; }
    .badge-danger { background: rgba(239,68,68,0.12); color: #991b1b; }
    .loading-card {
        display: grid;
        grid-template-columns: 1fr;
        gap: 18px;
        align-items: center;
        text-align: center;
    }
    .loading-dots {
        display: inline-flex;
        gap: 8px;
        justify-content: center;
    }
    .loading-dots span {
        width: 12px;
        height: 12px;
        border-radius: 999px;
        background: #2563eb;
        animation: bounce 1.15s infinite ease-in-out;
    }
    .loading-dots span:nth-child(2) { animation-delay: 0.15s; }
    .loading-dots span:nth-child(3) { animation-delay: 0.3s; }
    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); opacity: 0.55; }
        40% { transform: translateY(-10px); opacity: 1; }
    }
    .primary-gradient-button > button {
        border-radius: 18px;
        padding: 14px 28px;
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
        background: linear-gradient(135deg, #2563eb, #14b8a6);
        border: none;
        box-shadow: 0 20px 40px rgba(37,99,235,0.18);
        transition: transform 180ms ease, box-shadow 180ms ease;
    }
    .primary-gradient-button > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 26px 50px rgba(37,99,235,0.22);
    }
    .primary-gradient-button > button:focus {
        outline: none;
        box-shadow: 0 0 0 4px rgba(37,99,235,0.18);
    }
    .footer-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 12px;
        padding: 16px 20px;
        margin-top: 42px;
        border-top: 1px solid rgba(15,23,42,0.08);
        color: #475569;
        font-size: 0.93rem;
    }
    .footer-bar strong { color: #0f172a; }
    .section-divider {
        height: 1px;
        background: rgba(15,23,42,0.08);
        margin: 28px 0;
    }
    .report-card {
        border-radius: 20px;
        padding: 22px;
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(15,23,42,0.06);
        box-shadow: 0 18px 35px rgba(15,23,42,0.06);
    }
    .section-heading {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 18px;
    }
    .section-heading h2 {
        margin: 0;
        font-size: 1.5rem;
    }
    .section-heading p {
        margin: 0;
        color: #64748b;
        font-size: 0.95rem;
    }
    .stCheckbox label {
        font-weight: 600;
    }
    .stCheckbox input:checked + label {
        color: #15803d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# 2. SECURE GATEKEEPER & INFRASTRUCTURE LAYER
# -------------------------------------------------------------
# Extract key securely from Streamlit Cloud Secrets or OS Environment
env_key = ""
if "GEMINI_API_KEY" in st.secrets:
    env_key = st.secrets["GEMINI_API_KEY"].strip()
elif os.environ.get("GEMINI_API_KEY"):
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()

# Fallback to an interactive secure widget if Secrets are not configured
if not env_key:
    st.sidebar.markdown(
        """
        <div class='sidebar-panel'>
            <div class='sidebar-brand'>
                <div class='brand-icon'>🌧️</div>
                <div>
                    <h2>Disaster Management</h2>
                    <div style='color:#64748b;font-size:0.92rem;margin-top:4px;'>Enterprise command center</div>
                </div>
            </div>
            <div class='sidebar-divider'></div>
            <a class='sidebar-link' href='#dashboard'>🏠 Dashboard</a>
            <a class='sidebar-link' href='#preparedness'>🛡️ Preparedness</a>
            <a class='sidebar-link' href='#checklist'>📋 Emergency Checklist</a>
            <a class='sidebar-link' href='#travel'>🚗 Travel Advisory</a>
            <a class='sidebar-link' href='#settings'>⚙️ Settings</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("### 🔑 Authentication Setup")
    user_api_key = st.sidebar.text_input(
        label="Enter Gemini API Key to activate:",
        type="password",
        help="Paste your Google Cloud or AI Studio API key here.",
    )
else:
    st.sidebar.markdown(
        """
        <div class='sidebar-panel'>
            <div class='sidebar-brand'>
                <div class='brand-icon'>✅</div>
                <div>
                    <h2>Secure Gateway</h2>
                    <div style='color:#64748b;font-size:0.92rem;margin-top:4px;'>API key detected</div>
                </div>
            </div>
            <div class='sidebar-divider'></div>
            <a class='sidebar-link' href='#dashboard'>🏠 Dashboard</a>
            <a class='sidebar-link' href='#preparedness'>🛡️ Preparedness</a>
            <a class='sidebar-link' href='#checklist'>📋 Emergency Checklist</a>
            <a class='sidebar-link' href='#travel'>🚗 Travel Advisory</a>
            <a class='sidebar-link' href='#settings'>⚙️ Settings</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    user_api_key = env_key

# Stop execution gracefully if no key is provided anywhere
if not user_api_key:
    st.warning("⚠️ Waiting for Gemini API Key...")
    st.info("💡 **Developer Check:** Please add your API key in the Streamlit Cloud Settings -> Secrets, or paste it in the sidebar.")
    st.stop()

@st.cache_resource(show_spinner=False)
def initialize_client(validated_key: str) -> genai.Client:
    """
    Initializes the client on the public Generative Language endpoint.
    Crucial: vertexai=False allows standard API keys to authenticate.
    """
    return genai.Client(api_key=validated_key.strip(), vertexai=False)

try:
    client = initialize_client(user_api_key)
except Exception as init_err:
    st.error(f"System Infrastructure failure during client setup: {init_err}")
    st.stop()

# -------------------------------------------------------------
# 3. MAIN DASHBOARD UI
# -------------------------------------------------------------
st.markdown("<div id='dashboard'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class='hero-panel'>
        <div class='hero-content'>
            <p style='margin:0;font-size:0.95rem;font-weight:600;opacity:0.92;'>Enterprise Monsoon Preparedness Console</p>
            <h1 class='hero-title'>Premium Crisis Response Intelligence</h1>
            <p class='hero-subtitle'>Deliver high-confidence safety plans, travel advisories, emergency readiness checklists, and real-time family protection guidance powered by Gemini AI.</p>
            <div class='hero-pill-grid'>
                <div class='hero-pill'><span>☁️</span>Weather Status</div>
                <div class='hero-pill'><span>🏡</span>Family Safety</div>
                <div class='hero-pill'><span>🚨</span>Emergency Readiness</div>
                <div class='hero-pill'><span>🤖</span>AI Assistance</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

col_top1, col_top2, col_top3, col_top4 = st.columns(4, gap='large')
col_top1.markdown(
    """
    <div class='metric-card'>
        <h4>Current Alert Level</h4>
        <p>Yellow</p>
    </div>
    """,
    unsafe_allow_html=True,
)
col_top2.markdown(
    """
    <div class='metric-card'>
        <h4>Preparedness Score</h4>
        <p>78%</p>
    </div>
    """,
    unsafe_allow_html=True,
)
col_top3.markdown(
    """
    <div class='metric-card'>
        <h4>Family Risk Level</h4>
        <p>Moderate</p>
    </div>
    """,
    unsafe_allow_html=True,
)
col_top4.markdown(
    """
    <div class='metric-card'>
        <h4>AI Confidence</h4>
        <p>92%</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

with st.form(key="monsoon_assistance_form", clear_on_submit=False):
    st.markdown("<div class='glass-card'><h3>📋 Citizen Context Profiling</h3></div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns([1, 1], gap='large')
    with col_a:
        location = st.text_input(
            label="Your Current City / Region / Neighborhood Location:",
            value="Pune, Maharashtra",
            help="Allows the system to map terrain-specific travel vulnerabilities or localized flooding advisories."
        )
        family_context = st.text_area(
            label="Family Composition Details (Include elderly, children, pets, or medical requirements):",
            placeholder="e.g., 4 family members including an elderly grandparent who uses a wheelchair and a 14-month-old infant.",
            help="Tailors food, medical supplies, and immediate structural evacuation priorities."
        )
    
    with col_b:
        st.markdown(
            "<div class='glass-card'><h3>🧭 Scenario Settings</h3><p style='margin:0 0 14px 0;color:#475569;'>Fine-tune the advisory output for the right level of urgency.</p></div>",
            unsafe_allow_html=True,
        )
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
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    col_button, _ = st.columns([1, 3])
    with col_button:
        submit_btn = st.form_submit_button(label="🚀 Generate Critical Action Plan")

# -------------------------------------------------------------
# 4. CRISIS PROCESSING RUNTIME ROUTINE
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

    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1
            ),
        )

        if not response.text:
            raise ValueError("Null output payload returned from server gateway.")

        data = json.loads(response.text)
        progress_placeholder.progress(100)
        loading_placeholder.empty()

        st.markdown("<div id='preparedness'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='section-heading'>
                <div>
                    <h2>🚨 Alert & Preparedness Overview</h2>
                    <p>Actionable insights, safety cards, and AI confidence grouped for high-velocity decision making.</p>
                </div>
                <span class='badge-pill badge-warning'>Live advisory</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='result-grid'>
                <div class='result-card'>
                    <div class='card-icon' style='background: rgba(239,68,68,0.12); color:#b91c1c;'>🚨</div>
                    <h3>Alert</h3>
                    <p style='color:#0f172a; line-height:1.7;'>%s</p>
                </div>
                <div class='result-card'>
                    <div class='card-icon' style='background: rgba(37,99,235,0.12); color:#1d4ed8;'>🏠</div>
                    <h3>Home Safety</h3>
                    <p style='color:#0f172a; line-height:1.7;'>%s</p>
                </div>
                <div class='result-card'>
                    <div class='card-icon' style='background: rgba(34,197,94,0.12); color:#15803d;'>💊</div>
                    <h3>Medical</h3>
                    <p style='color:#0f172a; line-height:1.7;'>%s</p>
                </div>
                <div class='result-card'>
                    <div class='card-icon' style='background: rgba(14,165,233,0.12); color:#0369a1;'>🌧️</div>
                    <h3>Weather</h3>
                    <p style='color:#0f172a; line-height:1.7;'>%s</p>
                </div>
                <div class='result-card'>
                    <div class='card-icon' style='background: rgba(234,179,8,0.12); color:#b45309;'>🚗</div>
                    <h3>Travel</h3>
                    <p style='color:#0f172a; line-height:1.7;'>%s</p>
                </div>
                <div class='result-card'>
                    <div class='card-icon' style='background: rgba(16,185,129,0.12); color:#065f46;'>🧼</div>
                    <h3>Hygiene</h3>
                    <p style='color:#0f172a; line-height:1.7;'>%s</p>
                </div>
            </div>
            """ % (
                data['alert_banner'].get('headline', 'CRITICAL NOTICE'),
                data['personalized_preparedness_plan'].get('structural_safety', 'N/A'),
                data['personalized_preparedness_plan'].get('medical_provisions', 'N/A'),
                data.get('weather_aware_guidance', 'N/A'),
                data.get('travel_advisory', 'N/A'),
                data.get('safety_recommendations', 'N/A'),
            ),
            unsafe_allow_html=True,
        )

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div id='checklist'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='section-heading'>
                <div>
                    <h2>📋 Emergency Checklist</h2>
                    <p>Monitor completion progress for your family’s critical preparedness steps.</p>
                </div>
                <span class='badge-pill badge-success'>Checklist ready</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        checklist_items = data.get('emergency_checklist', [])
        if checklist_items:
            checked_items = 0
            for idx, item in enumerate(checklist_items):
                checked = st.checkbox(item, key=f"monsoon_item_{idx}")
                if checked:
                    checked_items += 1
            completion = int((checked_items / len(checklist_items)) * 100) if checklist_items else 0
            st.progress(completion)
            st.markdown(f"**Completion:** {completion}% of checklist items reviewed and acknowledged.")
        else:
            st.info("No explicit checklist items generated. Please regenerate with more family context.")

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown("<div id='travel'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='report-card'>
                <h3>📍 Travel Advisory & Safety Controls</h3>
                <p style='margin:0;color:#475569; line-height:1.8;'>%s</p>
                <div style='margin-top:18px; display:flex; flex-wrap:wrap; gap:12px;'>
                    <span class='badge-pill badge-warning'>Flood Routes</span>
                    <span class='badge-pill badge-danger'>Evacuation Ready</span>
                    <span class='badge-pill badge-success'>Sanitation Safe</span>
                </div>
            </div>
            """ % data.get('travel_advisory', 'N/A'),
            unsafe_allow_html=True,
        )

        st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='report-card'>
                <h3>🧠 AI Guidance Summary</h3>
                <p style='margin:0;color:#475569; line-height:1.8;'>%s</p>
            </div>
            """ % data.get('weather_aware_guidance', 'N/A'),
            unsafe_allow_html=True,
        )

        if st.button("🔄 Generate Again with same inputs", key="regen_action"):
            st.experimental_rerun()

        st.markdown(
            "<div class='footer-bar'>"
            "<span>Powered by Gemini AI · Streamlit · Disaster Management Dashboard</span>"
            "<span>Last Updated: %s</span>"
            "</div>" % datetime.now().strftime("%b %d, %Y • %I:%M %p"),
            unsafe_allow_html=True,
        )

    except json.JSONDecodeError:
        loading_placeholder.empty()
        progress_placeholder.empty()
        st.error("⚠️ Data interpretation anomaly: The response payload dropped broken segments. Please regenerate.")
    except Exception as runtime_error:
        loading_placeholder.empty()
        progress_placeholder.empty()
        st.error(f"❌ Operational lifecycle breakdown encountered: {runtime_error}")
        st.info("💡 *Developer Note:* If you see a 401/Blocked error, ensure the **Generative Language API** is enabled in your Google Cloud Project console.")
