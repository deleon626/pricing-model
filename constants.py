"""
Constants and default values for the Lapis Visuals Pricing Calculator.
"""

# Pricing thresholds and multipliers
PRODUCER_FEE_THRESHOLD = 20000000  # Projects < 20M don't get producer fee
RECOMMENDED_PRICE_MARGIN = 1.12  # 12% margin for recommended price

# Default rates (fallback if rates.json is not found)
DEFAULT_RATES = {
    "scriptwriting": {"base": 2000000, "complexity_factors": {"simple": 0.5, "standard": 1.0, "complex": 1.5}},
    "storyboard": {"base": 1500000},
    "location": {
        "none": 0,
        "Studio (1.5 M)": 1500000,
        "Styled Home (6 M)": 6000000,
        "Rooftop Café (4.5 M)": 4500000
    },
    "crew_roles": {
        "Director": 3000000,
        "DOP": 2500000,
        "Camera Assistant": 1000000,
        "Gaffer": 1200000,
        "Sound Engineer": 1500000,
        "Production Assistant": 800000
    },
    "equipment": {
        "basic": 5000000,
        "premium": 10000000
    },
    "post_production": {
        "editing": {"per_minute": 2000000, "complexity": {"simple": 0.8, "standard": 1.0, "complex": 1.3}},
        "color": {"per_minute": 1000000, "complexity": {"simple": 0.8, "standard": 1.0, "complex": 1.3}},
        "sfx": {"per_minute": 800000, "complexity": {"simple": 0.7, "standard": 1.0, "complex": 1.5}}
    },
    "producer_fee": {"percent": 0.075},
    "contingency": {"default": 0.10}
}

# Default questionnaire values
DEFAULT_QUESTIONNAIRE = {
    "video_length": 2.0,
    "deliverables": 1,
    "distribution": [],
    "format": "",
    "special_requirements": [],
    "concept": "",
    "shoot_date": None,
    "delivery_date": None,
    "budget_min": None,
    "budget_max": None
}

# Default production variables
DEFAULT_PRODUCTION_VARS = {
    "shooting_days": 1.0,
    "crew_size": 5,
    "location": "none",
    "talent_count": 1,
    "agency_markup": False,
    "props_design": "basic",
    "footage_volume": "standard",
    "contingency": 10
}

# UI constants
DISTRIBUTION_CHANNELS = ["Instagram", "TikTok", "YouTube", "LinkedIn", "Website", "TV/Broadcast"]
VIDEO_FORMATS = ["Commercial", "Documentary", "Event Coverage", "Social Media", "Corporate", "Training"]
SPECIAL_REQUIREMENTS = ["SFX", "Motion Graphics", "Green Screen", "Aerial Shots", "Underwater"]
LOCATION_TYPES = ["none", "Studio (1.5 M)", "Styled Home (6 M)", "Rooftop Café (4.5 M)"]
PROPS_DESIGN_LEVELS = ["basic", "custom", "elaborate"]
FOOTAGE_VOLUME_LEVELS = ["low", "standard", "high"]
USER_ROLES = ["Account Manager", "Producer / PM", "Finance", "Client"] 