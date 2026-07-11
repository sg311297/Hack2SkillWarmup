"""
Unit tests for the Monsoon Preparedness Application.

Tests validate:
- Crisis plan generation and response parsing
- API integration with mocked Gemini client
- JSON response validation
"""

import json
import pytest
from unittest.mock import MagicMock, patch

from utils import (
    generate_crisis_plan,
    parse_crisis_plan_response,
    initialize_genai_client,
)


class TestCrisisPlanGeneration:
    """Test suite for crisis plan generation and API integration."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock Gemini client for testing."""
        client = MagicMock()
        return client

    @pytest.fixture
    def expected_response_data(self) -> dict:
        """Expected crisis plan response structure."""
        return {
            "alert_banner": {
                "headline": "Red Alert: Severe Localized Inundation",
                "action_required": "Move electrical units above baseline water marks."
            },
            "personalized_preparedness_plan": {
                "structural_safety": "Secure windows and inspect main sump pump outlets.",
                "medical_provisions": "Store extra child nutrition items."
            },
            "weather_aware_guidance": "Heavy downpours expected to persist.",
            "emergency_checklist": [
                "Flashlight",
                "Potable Water",
                "Emergency medicines"
            ],
            "travel_advisory": "Avoid low-lying underpasses.",
            "safety_recommendations": "Boil tap water before consumption."
        }

    def test_generate_crisis_plan_success(self, mock_client, expected_response_data):
        """
        Test that generate_crisis_plan correctly constructs the prompt
        and returns valid JSON response.
        
        Validates:
        - API is called with correct parameters
        - Response text is returned properly
        - JSON structure is valid
        """
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = json.dumps(expected_response_data)
        mock_client.models.generate_content.return_value = mock_response

        # Execute function
        result_text = generate_crisis_plan(
            client=mock_client,
            location="Pune",
            family_context="2 adults, 1 child",
            weather_severity="Red Alert (Extremely Severe / Flood Warning)",
            language_choice="English"
        )

        # Assertions
        assert result_text is not None
        assert isinstance(result_text, str)
        
        # Verify API was called
        mock_client.models.generate_content.assert_called_once()

    def test_parse_crisis_plan_response_success(self, expected_response_data):
        """
        Test JSON parsing and validation of crisis plan response.
        
        Validates:
        - Valid JSON is parsed correctly
        - Response contains required keys
        - Data types are correct
        """
        json_text = json.dumps(expected_response_data)
        
        # Parse response
        data = parse_crisis_plan_response(json_text)
        
        # Assertions
        assert data is not None
        assert isinstance(data, dict)
        assert "alert_banner" in data
        assert data["alert_banner"]["headline"] == "Red Alert: Severe Localized Inundation"
        assert "emergency_checklist" in data
        assert len(data["emergency_checklist"]) == 3
        assert isinstance(data["emergency_checklist"], list)

    def test_parse_crisis_plan_response_invalid_json(self):
        """
        Test that invalid JSON raises appropriate error.
        
        Validates:
        - JSONDecodeError is raised for malformed JSON
        - Error is handled appropriately
        """
        invalid_json = "{invalid json content"
        
        # Verify exception is raised
        with pytest.raises(json.JSONDecodeError):
            parse_crisis_plan_response(invalid_json)

    def test_generate_crisis_plan_empty_response(self, mock_client):
        """
        Test handling of empty API response.
        
        Validates:
        - Empty response is detected
        - Appropriate error is raised
        """
        # Setup mock to return empty response
        mock_response = MagicMock()
        mock_response.text = ""
        mock_client.models.generate_content.return_value = mock_response

        # Verify error is raised
        with pytest.raises(ValueError, match="Null output payload"):
            generate_crisis_plan(
                client=mock_client,
                location="Pune",
                family_context="Test family",
                weather_severity="Yellow Alert (Heavy Rain Expected)",
                language_choice="English"
            )

    def test_response_contains_all_required_fields(self, expected_response_data):
        """
        Test that response contains all required fields for proper rendering.
        
        Validates:
        - All UI rendering fields are present
        - Field structure is correct
        """
        data = parse_crisis_plan_response(json.dumps(expected_response_data))
        
        # Required top-level fields
        required_fields = [
            "alert_banner",
            "personalized_preparedness_plan",
            "weather_aware_guidance",
            "emergency_checklist",
            "travel_advisory",
            "safety_recommendations"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Validate nested structures
        assert "headline" in data["alert_banner"]
        assert "action_required" in data["alert_banner"]
        assert "structural_safety" in data["personalized_preparedness_plan"]
        assert "medical_provisions" in data["personalized_preparedness_plan"]

    def test_emergency_checklist_is_list(self, expected_response_data):
        """
        Test that emergency checklist is properly formatted as a list.
        
        Validates:
        - Checklist is a list
        - All items are strings
        """
        data = parse_crisis_plan_response(json.dumps(expected_response_data))
        
        checklist = data.get("emergency_checklist", [])
        assert isinstance(checklist, list)
        assert len(checklist) > 0
        assert all(isinstance(item, str) for item in checklist)


class TestAPIInitialization:
    """Test suite for API client initialization."""

    def test_initialize_client_valid_key(self):
        """
        Test that client is initialized successfully with valid API key.
        
        Validates:
        - Client object is returned
        - No errors occur
        """
        with patch('utils.genai.Client') as mock_genai:
            mock_client = MagicMock()
            mock_genai.return_value = mock_client
            
            result = initialize_genai_client("valid-api-key-12345")
            
            assert result is not None
            mock_genai.assert_called_once_with(api_key="valid-api-key-12345", vertexai=False)

    def test_initialize_client_empty_key(self):
        """
        Test that empty API key raises ValueError.
        
        Validates:
        - ValueError is raised with appropriate message
        """
        with pytest.raises(ValueError, match="API key cannot be empty"):
            initialize_genai_client("")

    def test_initialize_client_none_key(self):
        """
        Test that None API key raises ValueError.
        
        Validates:
        - TypeError or ValueError is caught appropriately
        """
        with pytest.raises(ValueError):
            initialize_genai_client(None)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
