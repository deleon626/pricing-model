"""
Pricing calculation logic for the Lapis Visuals Pricing Calculator.
"""

import json
from typing import Dict, Tuple, List, Any
from constants import DEFAULT_RATES, PRODUCER_FEE_THRESHOLD, RECOMMENDED_PRICE_MARGIN

def load_rates():
    """
    Load rates from rates.json file or return default rates if file not found.
    
    Returns:
        Dict: Dictionary containing all rate information
    """
    try:
        with open("rates.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return default rates if file not found
        return DEFAULT_RATES

def calculate_quote(questionnaire: Dict[str, Any], production_vars: Dict[str, Any], rates: Dict[str, Any]) -> Tuple[int, int, int]:
    """
    Calculate the low, high, and recommended price quotes based on questionnaire and production variables.
    
    Args:
        questionnaire: Dictionary containing questionnaire responses
        production_vars: Dictionary containing production variables
        rates: Dictionary containing rate information
        
    Returns:
        Tuple of (low_quote, high_quote, recommended_quote) as integers
    """
    q = questionnaire
    p = production_vars
    
    # Base calculation factors
    complexity_factor = 1.0
    if "Motion Graphics" in q["special_requirements"]:
        complexity_factor += 0.2
    if "Green Screen" in q["special_requirements"]:
        complexity_factor += 0.15
    if "SFX" in q["special_requirements"]:
        complexity_factor += 0.1
    if "Aerial Shots" in q["special_requirements"]:
        complexity_factor += 0.2
    
    # Calculate Pre-production costs
    scriptwriting_low = rates["scriptwriting"]["base"] * rates["scriptwriting"]["complexity_factors"]["simple"]
    scriptwriting_high = rates["scriptwriting"]["base"] * rates["scriptwriting"]["complexity_factors"]["complex"]
    
    storyboard_low = rates["storyboard"]["base"] * q["deliverables"] * 0.8
    storyboard_high = rates["storyboard"]["base"] * q["deliverables"] * 1.2
    
    location_cost = rates["location"][p["location"]]
    
    # Production costs
    crew_cost_low = sum(list(rates["crew_roles"].values())[:p["crew_size"]]) * p["shooting_days"]
    crew_cost_high = crew_cost_low * 1.2
    
    equipment_low = rates["equipment"]["basic"] * p["shooting_days"]
    equipment_high = rates["equipment"]["premium"] * p["shooting_days"]
    
    talent_low = p["talent_count"] * 1000000 * (1.1 if p["agency_markup"] else 1.0)
    talent_high = p["talent_count"] * 2000000 * (1.3 if p["agency_markup"] else 1.0)
    
    props_low = 2000000 if p["props_design"] == "basic" else 3000000 if p["props_design"] == "custom" else 5000000
    props_high = 3000000 if p["props_design"] == "basic" else 5000000 if p["props_design"] == "custom" else 8000000
    
    # Post-production costs
    editing_factor = 0.8 if p["footage_volume"] == "low" else 1.0 if p["footage_volume"] == "standard" else 1.3
    
    post_low = (
        rates["post_production"]["editing"]["per_minute"] * q["video_length"] * editing_factor * 
        rates["post_production"]["editing"]["complexity"]["simple"] +
        rates["post_production"]["color"]["per_minute"] * q["video_length"] * 
        rates["post_production"]["color"]["complexity"]["simple"] +
        rates["post_production"]["sfx"]["per_minute"] * q["video_length"] * 
        rates["post_production"]["sfx"]["complexity"]["simple"]
    )
    
    post_high = (
        rates["post_production"]["editing"]["per_minute"] * q["video_length"] * editing_factor * 
        rates["post_production"]["editing"]["complexity"]["complex"] +
        rates["post_production"]["color"]["per_minute"] * q["video_length"] * 
        rates["post_production"]["color"]["complexity"]["complex"] +
        rates["post_production"]["sfx"]["per_minute"] * q["video_length"] * 
        rates["post_production"]["sfx"]["complexity"]["complex"]
    )
    
    # Sum up pre-contingency total
    low_subtotal = (
        scriptwriting_low + storyboard_low + location_cost + 
        crew_cost_low + equipment_low + talent_low + props_low + post_low
    )
    
    high_subtotal = (
        scriptwriting_high + storyboard_high + location_cost + 
        crew_cost_high + equipment_high + talent_high + props_high + post_high
    )
    
    # Admin/Producer fee (exclude for projects < Rp 20M)
    if low_subtotal >= PRODUCER_FEE_THRESHOLD:
        producer_fee_low = low_subtotal * rates["producer_fee"]["percent"]
        producer_fee_high = high_subtotal * rates["producer_fee"]["percent"]
    else:
        producer_fee_low = producer_fee_high = 0
    
    # Add contingency
    contingency_percent = p["contingency"] / 100
    contingency_low = low_subtotal * contingency_percent
    contingency_high = high_subtotal * contingency_percent
    
    # Final totals
    low_quote = low_subtotal + producer_fee_low + contingency_low
    high_quote = high_subtotal + producer_fee_high + contingency_high
    
    # Recommended is median + a margin (12% as per design)
    recommended = ((low_quote + high_quote) / 2) * RECOMMENDED_PRICE_MARGIN
    
    return int(low_quote), int(high_quote), int(recommended)

def generate_line_items(questionnaire: Dict[str, Any], production_vars: Dict[str, Any], rates: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    """
    Generate detailed line items for the quote.
    
    Args:
        questionnaire: Dictionary containing questionnaire responses
        production_vars: Dictionary containing production variables
        rates: Dictionary containing rate information
        
    Returns:
        Dictionary mapping categories to their low and high estimates
    """
    q = questionnaire
    p = production_vars
    
    # Calculate quote values for producer fee and contingency
    low_quote, high_quote, _ = calculate_quote(q, p, rates)
    
    items = {
        "Pre-production": {
            "low": rates["scriptwriting"]["base"] * rates["scriptwriting"]["complexity_factors"]["simple"] + 
                  rates["storyboard"]["base"] * q["deliverables"] * 0.8,
            "high": rates["scriptwriting"]["base"] * rates["scriptwriting"]["complexity_factors"]["complex"] + 
                   rates["storyboard"]["base"] * q["deliverables"] * 1.2
        },
        "Crew Costs": {
            "low": sum(list(rates["crew_roles"].values())[:p["crew_size"]]) * p["shooting_days"],
            "high": sum(list(rates["crew_roles"].values())[:p["crew_size"]]) * p["shooting_days"] * 1.2
        },
        "Equipment": {
            "low": rates["equipment"]["basic"] * p["shooting_days"],
            "high": rates["equipment"]["premium"] * p["shooting_days"]
        },
        "Location": {
            "low": rates["location"][p["location"]],
            "high": rates["location"][p["location"]]
        },
        "Talent": {
            "low": p["talent_count"] * 1000000 * (1.1 if p["agency_markup"] else 1.0),
            "high": p["talent_count"] * 2000000 * (1.3 if p["agency_markup"] else 1.0)
        },
        "Post-production": {
            "low": q["video_length"] * 3000000,
            "high": q["video_length"] * 5000000
        },
        "Producer Fee": {
            "low": low_quote * rates["producer_fee"]["percent"] if low_quote >= PRODUCER_FEE_THRESHOLD else 0,
            "high": high_quote * rates["producer_fee"]["percent"] if high_quote >= PRODUCER_FEE_THRESHOLD else 0
        },
        "Contingency": {
            "low": low_quote * (p["contingency"] / 100),
            "high": high_quote * (p["contingency"] / 100)
        }
    }
    
    return items 