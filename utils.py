"""
Utility functions for UI generation and API interactions.
Abstracts common UI patterns and API logic.
"""

import json
import logging
from typing import Any, Optional
from datetime import datetime

import streamlit as st
from google import genai
from google.genai import types
import html as html_lib
import re

from config import (
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
    RESPONSE_KEYS,
    UI_LABELS,
    HELP_TEXTS,
    ERROR_MESSAGES,
)

# Configure logging
logger = logging.getLogger(__name__)


def clean_model_field(raw: Optional[str]) -> str:
    """
    Clean and normalize text returned by the model.

    - Strips surrounding backticks or code fences
    - Unescapes HTML entities (e.g. &lt;, &gt;)
    - Trims whitespace

    Returns a safe plain-text string suitable for insertion into HTML templates
    that the app constructs (not for rendering untrusted HTML directly).
    """
    if not raw:
        return ""
    text = str(raw).strip()
    # Remove common markdown/code fences/backticks
    # Remove leading/trailing triple backticks or single backticks
    text = re.sub(r"^`{1,3}|`{1,3}$", "", text).strip()
    # If wrapped in fenced code blocks with language (```json ... ```)
    text = re.sub(r"^```[a-zA-Z0-9\-]*\n|\n```$", "", text)
    # Unescape HTML entities
    text = html_lib.unescape(text)
    return text


def render_sidebar_panel(title: str, subtitle: str, icon: str, is_authenticated: bool) -> None:
    """
    Render a branded sidebar panel.
    
    Args:
        title: Main title text
        subtitle: Subtitle text
        icon: Emoji icon for the brand
        is_authenticated: Whether API is authenticated
    """
    brand_icon = "✅" if is_authenticated else icon
    nav_html = """
    <div class='sidebar-panel'>
        <div class='sidebar-brand'>
            <div class='brand-icon'>{}</div>
            <div>
                <h2>{}</h2>
                <div style='color:#64748b;font-size:0.92rem;margin-top:4px;'>{}</div>
            </div>
        </div>
        <div class='sidebar-divider'></div>
        <a class='sidebar-link' href='#dashboard'>🏠 Dashboard</a>
        <a class='sidebar-link' href='#preparedness'>🛡️ Preparedness</a>
        <a class='sidebar-link' href='#checklist'>📋 Emergency Checklist</a>
        <a class='sidebar-link' href='#travel'>🚗 Travel Advisory</a>
        <a class='sidebar-link' href='#settings'>⚙️ Settings</a>
    </div>
    """.format(brand_icon, title, subtitle)
    st.sidebar.markdown(nav_html, unsafe_allow_html=True)


def render_hero_section(title: str, subtitle: str, pills: list[str]) -> None:
    """
    Render the hero banner section.
    
    Args:
        title: Main heading
        subtitle: Descriptive text
        pills: List of pill items to display
    """
    pills_html = "".join(
        f"<div class='hero-pill'><span>{p.split(maxsplit=1)[0]}</span>{' '.join(p.split()[1:])}</div>"
        for p in pills
    )
    hero_html = f"""
    <div class='hero-panel'>
        <div class='hero-content'>
            <p style='margin:0;font-size:0.95rem;font-weight:600;opacity:0.92;'>Enterprise Monsoon Preparedness Console</p>
            <h1 class='hero-title'>{title}</h1>
            <p class='hero-subtitle'>{subtitle}</p>
            <div class='hero-pill-grid'>
                {pills_html}
            </div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)


def render_metrics(metrics: list[dict[str, str]]) -> None:
    """
    Render metric cards in a 4-column layout.
    
    Args:
        metrics: List of dicts with 'title' and 'value' keys
    """
    cols = st.columns(4, gap="large")
    for idx, metric in enumerate(metrics):
        with cols[idx]:
            metric_html = f"""
            <div class='metric-card'>
                <h4>{metric['title']}</h4>
                <p>{metric['value']}</p>
            </div>
            """
            st.markdown(metric_html, unsafe_allow_html=True)


def render_result_grid(data: dict[str, Any]) -> None:
    """
    Render the results grid with 6 cards.
    
    Args:
        data: Response data dictionary from API
    """
    results = [
        {
            "icon": "🚨",
            "title": "Alert",
            "content": data.get(RESPONSE_KEYS["alert_banner"], {}).get("headline", "N/A"),
            "bg_color": "rgba(239,68,68,0.12)",
            "icon_color": "#b91c1c",
        },
        {
            "icon": "🏠",
            "title": "Home Safety",
            "content": data.get(RESPONSE_KEYS["preparedness_plan"], {}).get(RESPONSE_KEYS["structural_safety"], "N/A"),
            "bg_color": "rgba(37,99,235,0.12)",
            "icon_color": "#1d4ed8",
        },
        {
            "icon": "💊",
            "title": "Medical",
            "content": data.get(RESPONSE_KEYS["preparedness_plan"], {}).get(RESPONSE_KEYS["medical_provisions"], "N/A"),
            "bg_color": "rgba(34,197,94,0.12)",
            "icon_color": "#15803d",
        },
        {
            "icon": "🌧️",
            "title": "Weather",
            "content": data.get(RESPONSE_KEYS["weather_guidance"], "N/A"),
            "bg_color": "rgba(14,165,233,0.12)",
            "icon_color": "#0369a1",
        },
        {
            "icon": "🚗",
            "title": "Travel",
            "content": data.get(RESPONSE_KEYS["travel_advisory"], "N/A"),
            "bg_color": "rgba(234,179,8,0.12)",
            "icon_color": "#b45309",
        },
        {
            "icon": "🧼",
            "title": "Hygiene",
            "content": data.get(RESPONSE_KEYS["safety_recommendations"], "N/A"),
            "bg_color": "rgba(16,185,129,0.12)",
            "icon_color": "#065f46",
        },
    ]
    
    cards_html = ""
    for result in results:
        content = clean_model_field(result.get("content", ""))
        cards_html += f"""
        <div class='result-card'>
            <div class='card-icon' style='background: {result["bg_color"]}; color:{result["icon_color"]};'>{result["icon"]}</div>
            <h3>{result["title"]}</h3>
            <p style='color:#0f172a; line-height:1.7;'>{content}</p>
        </div>
        """
    
    st.markdown(
        f"<div class='result-grid'>{cards_html}</div>",
        unsafe_allow_html=True,
    )


def render_checklist(items: list[str]) -> None:
    """
    Render interactive checklist with progress tracking.
    
    Args:
        items: List of checklist items
    """
    if not items:
        st.info("No explicit checklist items generated. Please regenerate with more family context.")
        return
    
    checked_count = 0
    for idx, item in enumerate(items):
        checked = st.checkbox(
            label=item,
            key=f"monsoon_item_{idx}",
            help=f"Mark '{item}' as completed in your emergency checklist.",
        )
        if checked:
            checked_count += 1
    
    completion_percent = int((checked_count / len(items)) * 100) if items else 0
    st.progress(completion_percent)
    st.markdown(f"**Completion:** {completion_percent}% of checklist items reviewed and acknowledged.")


def render_footer(timestamp: Optional[datetime] = None) -> None:
    """
    Render the footer bar.
    
    Args:
        timestamp: Optional datetime to display, defaults to current time
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    footer_html = f"""
    <div class='footer-bar'>
        <span>Powered by Gemini AI · Streamlit · Disaster Management Dashboard</span>
        <span>Last Updated: {timestamp.strftime("%b %d, %Y • %I:%M %p")}</span>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


def get_api_key_from_secrets() -> Optional[str]:
    """
    Retrieve and validate API key from Streamlit secrets or environment.
    
    Returns:
        API key string or None if not found
    """
    try:
        if "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"].strip()
            if key:
                logger.info("API key loaded from Streamlit secrets")
                return key
    except Exception as e:
        logger.warning(f"Error reading from secrets: {e}")
    
    import os
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key:
        logger.info("API key loaded from environment variable")
        return key
    
    return None


def initialize_genai_client(api_key: str) -> genai.Client:
    """
    Initialize the Google GenAI client.
    
    Args:
        api_key: The API key for authentication
        
    Returns:
        Initialized GenAI client
        
    Raises:
        ValueError: If API key is empty
        Exception: If client initialization fails
    """
    if not api_key or not api_key.strip():
        raise ValueError("API key cannot be empty")
    
    logger.info("Initializing GenAI client")
    return genai.Client(api_key=api_key.strip(), vertexai=False)


def generate_crisis_plan(
    client: genai.Client,
    location: str,
    family_context: str,
    weather_severity: str,
    language_choice: str,
) -> str:
    """
    Generate a monsoon preparedness plan using Gemini API.
    
    Args:
        client: Initialized GenAI client
        location: User's location
        family_context: Description of family composition
        weather_severity: Current weather alert level
        language_choice: Preferred language for response
        
    Returns:
        JSON string containing the crisis plan
        
    Raises:
        ValueError: If response is empty
        Exception: If API call fails
    """
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

    IMPORTANT: Return only a single valid JSON object. DO NOT include any HTML tags, markdown, or
    code fences. All response fields must contain plain text only.
    """
    
    logger.info(f"Generating crisis plan for {location}")
    
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=GEMINI_TEMPERATURE,
            ),
        )
        
        if not response.text:
            logger.error("Empty response from API")
            raise ValueError(ERROR_MESSAGES["no_response"])
        
        logger.info("Crisis plan generated successfully")
        return response.text
        
    except Exception as e:
        logger.error(f"Error generating crisis plan: {e}")
        raise


def parse_crisis_plan_response(response_text: str) -> dict[str, Any]:
    """
    Parse and validate the crisis plan JSON response.
    
    Args:
        response_text: Raw JSON response text
        
    Returns:
        Parsed dictionary
        
    Raises:
        json.JSONDecodeError: If JSON is invalid
    """
    try:
        data = json.loads(response_text)
        logger.info("Crisis plan response parsed successfully")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        raise
