"""
Configuration module for Monsoon Preparedness Application.
Centralizes all constants and configuration settings.
"""

from typing import Final

# API Configuration
GEMINI_API_KEY_ENV: Final[str] = "GEMINI_API_KEY"
GEMINI_MODEL: Final[str] = "gemini-3.5-flash"
GEMINI_TEMPERATURE: Final[float] = 0.1
VERTEXAI_ENABLED: Final[bool] = False

# Application Configuration
APP_TITLE: Final[str] = "Monsoon Preparedness & Citizen Assistance Hub"
APP_ICON: Final[str] = "🌧️"
APP_LAYOUT: Final[str] = "wide"

# Page Sections
SECTION_IDS: Final[dict[str, str]] = {
    "dashboard": "dashboard",
    "preparedness": "preparedness",
    "checklist": "checklist",
    "travel": "travel",
    "settings": "settings",
}

# Weather Severity Options
WEATHER_SEVERITY_OPTIONS: Final[list[str]] = [
    "Normal / Pre-Monsoon Preparation",
    "Yellow Alert (Heavy Rain Expected)",
    "Orange Alert (Very Heavy Rain / Disruptions)",
    "Red Alert (Extremely Severe / Flood Warning)",
]

# Language Options
LANGUAGE_OPTIONS: Final[list[str]] = [
    "English",
    "Hindi (हिंदी)",
    "Marathi (मराठी)",
]

# Default Values
DEFAULT_LOCATION: Final[str] = "Pune, Maharashtra"
DEFAULT_ALERT_LEVEL: Final[str] = "Yellow"
DEFAULT_PREPAREDNESS_SCORE: Final[int] = 78
DEFAULT_RISK_LEVEL: Final[str] = "Moderate"
DEFAULT_AI_CONFIDENCE: Final[int] = 92

# JSON Response Schema Keys
RESPONSE_KEYS: Final[dict[str, str]] = {
    "alert_banner": "alert_banner",
    "action_required": "action_required",
    "headline": "headline",
    "preparedness_plan": "personalized_preparedness_plan",
    "structural_safety": "structural_safety",
    "medical_provisions": "medical_provisions",
    "weather_guidance": "weather_aware_guidance",
    "emergency_checklist": "emergency_checklist",
    "travel_advisory": "travel_advisory",
    "safety_recommendations": "safety_recommendations",
}

# UI Messages
ERROR_MESSAGES: Final[dict[str, str]] = {
    "no_api_key": "⚠️ Waiting for Gemini API Key...",
    "no_api_key_info": "💡 **Developer Check:** Please add your API key in the Streamlit Cloud Settings -> Secrets, or paste it in the sidebar.",
    "api_init_error": "System Infrastructure failure during client setup: {error}",
    "no_response": "Null output payload returned from server gateway.",
    "json_decode_error": "⚠️ Data interpretation anomaly: The response payload dropped broken segments. Please regenerate.",
    "runtime_error": "❌ Operational lifecycle breakdown encountered: {error}",
    "api_debug_note": "💡 *Developer Note:* If you see a 401/Blocked error, ensure the **Generative Language API** is enabled in your Google Cloud Project console.",
}

# UI Strings
UI_LABELS: Final[dict[str, str]] = {
    "location": "Your Current City / Region / Neighborhood Location:",
    "family_context": "Family Composition Details (Include elderly, children, pets, or medical requirements):",
    "severity": "Current Regional Weather Severity Status:",
    "language": "Select System Assistance Language Preferred:",
    "generate_button": "🚀 Generate Critical Action Plan",
    "regenerate_button": "🔄 Generate Again with same inputs",
}

# Help Texts
HELP_TEXTS: Final[dict[str, str]] = {
    "location": "Allows the system to map terrain-specific travel vulnerabilities or localized flooding advisories.",
    "family_context": "Tailors food, medical supplies, and immediate structural evacuation priorities.",
    "severity": "Sets the operational urgency context for before, during, or after severe weather events.",
    "language": "Ensures crucial safety instructions are fully accessible in the user's primary language.",
}

# Metrics Configuration
METRICS: Final[list[dict[str, str]]] = [
    {"title": "Current Alert Level", "value": "Yellow"},
    {"title": "Preparedness Score", "value": "78%"},
    {"title": "Family Risk Level", "value": "Moderate"},
    {"title": "AI Confidence", "value": "92%"},
]

# Badge Colors Configuration
BADGES: Final[dict[str, dict[str, str]]] = {
    "warning": {"class": "badge-warning", "text": "Live advisory"},
    "success": {"class": "badge-success", "text": "Checklist ready"},
    "info": {"class": "badge-info", "text": "Flood Routes"},
}
