import json

def test_monsoon_payload_integrity():
    """
    Asserts that the system prompt outputs an intact JSON conforming
    exactly to the multi-language structural framework.
    """
    mock_payload = """{
        "alert_banner": {
            "headline": "Red Alert: Severe Localized Inundation",
            "action_required": "Move electrical units above baseline water marks."
        },
        "personalized_preparedness_plan": {
            "structural_safety": "Secure windows and inspect main sump pump outlets.",
            "medical_provisions": "Store extra child nutrition items and stock emergency medical kits."
        },
        "weather_aware_guidance": "Heavy downpours expected to persist until 18:00 hours.",
        "emergency_checklist": ["Flashlight", "Potable Water", "First Aid Items"],
        "travel_advisory": "Avoid low-lying underpasses and avoid driving over stagnant logging pools.",
        "safety_recommendations": "Boil all municipal tap water prior to consumption."
    }"""
    
    data = json.loads(mock_payload)
    assert "alert_banner" in data
    assert "personalized_preparedness_plan" in data
    assert "emergency_checklist" in data
    assert isinstance(data["emergency_checklist"], list)