"""
Template handling for the Lapis Visuals Pricing Calculator.
"""

from typing import Dict, Any

def get_commercial_template() -> Dict[str, Dict[str, Any]]:
    """Return the commercial template settings."""
    return {
        "questionnaire": {
            "video_length": 1.0,
            "deliverables": 2,
            "distribution": ["Instagram", "YouTube", "Website"],
            "format": "Commercial",
            "special_requirements": ["Motion Graphics"],
            "concept": "Brand commercial highlighting key product features"
        },
        "production_vars": {
            "shooting_days": 1.0,
            "crew_size": 6,
            "location": "Studio (1.5 M)",
            "talent_count": 2,
            "agency_markup": True,
            "props_design": "custom",
            "footage_volume": "standard",
            "contingency": 10
        }
    }

def get_social_template() -> Dict[str, Dict[str, Any]]:
    """Return the social media template settings."""
    return {
        "questionnaire": {
            "video_length": 0.5,
            "deliverables": 3,
            "distribution": ["Instagram", "TikTok"],
            "format": "Social Media",
            "special_requirements": [],
            "concept": "Short social media snippets for product launch"
        },
        "production_vars": {
            "shooting_days": 0.5,
            "crew_size": 3,
            "location": "none",
            "talent_count": 1,
            "agency_markup": False,
            "props_design": "basic",
            "footage_volume": "low",
            "contingency": 5
        }
    }

def get_documentary_template() -> Dict[str, Dict[str, Any]]:
    """Return the documentary template settings."""
    return {
        "questionnaire": {
            "video_length": 10.0,
            "deliverables": 1,
            "distribution": ["YouTube", "Website"],
            "format": "Documentary",
            "special_requirements": ["Aerial Shots"],
            "concept": "Documentary style brand story covering company history"
        },
        "production_vars": {
            "shooting_days": 2.0,
            "crew_size": 5,
            "location": "Styled Home (6 M)",
            "talent_count": 4,
            "agency_markup": False,
            "props_design": "elaborate",
            "footage_volume": "high",
            "contingency": 15
        }
    }

def get_event_template() -> Dict[str, Dict[str, Any]]:
    """Return the event coverage template settings."""
    return {
        "questionnaire": {
            "video_length": 3.0,
            "deliverables": 2,
            "distribution": ["LinkedIn", "Website", "YouTube"],
            "format": "Event Coverage",
            "special_requirements": [],
            "concept": "Corporate event highlight reel"
        },
        "production_vars": {
            "shooting_days": 1.0,
            "crew_size": 4,
            "location": "none",
            "talent_count": 0,
            "agency_markup": False,
            "props_design": "basic",
            "footage_volume": "high",
            "contingency": 10
        }
    }

def load_template(template_type: str) -> Dict[str, Dict[str, Any]]:
    """
    Load a predefined template by name.
    
    Args:
        template_type: The template type to load ('commercial', 'social', 'documentary', 'event')
        
    Returns:
        Dictionary containing questionnaire and production_vars settings
    """
    if template_type == "commercial":
        return get_commercial_template()
    elif template_type == "social":
        return get_social_template()
    elif template_type == "documentary":
        return get_documentary_template()
    elif template_type == "event":
        return get_event_template()
    else:
        raise ValueError(f"Unknown template type: {template_type}") 