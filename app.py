import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# Import new modular components
from constants import (
    DEFAULT_QUESTIONNAIRE, DEFAULT_PRODUCTION_VARS,
    DISTRIBUTION_CHANNELS, VIDEO_FORMATS, SPECIAL_REQUIREMENTS,
    LOCATION_TYPES, PROPS_DESIGN_LEVELS, FOOTAGE_VOLUME_LEVELS
)
from pricing_logic import load_rates, calculate_quote, generate_line_items
from templates import load_template
from ui_components import (
    render_header, render_sidebar_user_role, render_sidebar_quote_summary,
    render_rate_card, render_template_buttons, render_questionnaire_form,
    render_production_form, render_detailed_breakdown, render_rates_editor
)
from export_utils import get_table_download_link, generate_pdf_html, get_pdf_download_button

# Set page configuration
st.set_page_config(
    page_title="Lapis Visuals - Pricing Calculator",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "questionnaire" not in st.session_state:
    st.session_state.questionnaire = DEFAULT_QUESTIONNAIRE.copy()

if "production_vars" not in st.session_state:
    st.session_state.production_vars = DEFAULT_PRODUCTION_VARS.copy()

# Load rates
rates = load_rates()

def load_rates_json():
    with open("LAPIS/pricing-model/rates.json", "r") as f:
        return json.load(f)

def save_rates_json(rates):
    with open("LAPIS/pricing-model/rates.json", "w") as f:
        json.dump(rates, f, indent=2)

def apply_template(template_type):
    """Apply a template to the session state"""
    template = load_template(template_type)
    st.session_state.questionnaire.update(template["questionnaire"])
    st.session_state.production_vars.update(template["production_vars"])
    st.rerun()

# Main app layout
def main():
    # Render sidebar components
    user_role = render_sidebar_user_role()
    
    # Calculate quote and render sidebar summary
    q = st.session_state.questionnaire
    p = st.session_state.production_vars
    low_quote, high_quote, recommended = calculate_quote(q, p, rates)
    line_items = generate_line_items(q, p, rates)
    
    render_sidebar_quote_summary(low_quote, high_quote, recommended, line_items)
    
    # Main page content
    render_header("Lapis Visuals - Pricing Calculator")
    
    # Render rate card in an expander
    render_rate_card(rates)
    
    # --- Rates Editor ---
    submitted = render_rates_editor(rates)
    if submitted:
        save_rates_json(rates)
        st.success("Rates updated! Please refresh or rerun the app.")
        st.experimental_rerun()
    
    st.markdown("---")
    
    # --- Client Questionnaire ---
    st.header("Client Questionnaire")
    
    # Render questionnaire form
    render_questionnaire_form(
        st.session_state.questionnaire,
        DISTRIBUTION_CHANNELS,
        VIDEO_FORMATS,
        SPECIAL_REQUIREMENTS
    )
    
    # Template buttons
    render_template_buttons(apply_template)
    
    st.markdown("---")
    
    # --- Production Variables ---
    st.header("Production Variables")
    
    # Render production form
    render_production_form(
        st.session_state.production_vars,
        LOCATION_TYPES,
        PROPS_DESIGN_LEVELS,
        FOOTAGE_VOLUME_LEVELS
    )
    
    st.markdown("---")
    
    # Create callback functions for export
    def pdf_callback():
        get_pdf_download_button(
            line_items,
            st.session_state.questionnaire,
            st.session_state.production_vars,
            low_quote, high_quote, recommended
        )
    
    def excel_callback():
        return get_table_download_link(
            line_items,
            st.session_state.questionnaire,
            st.session_state.production_vars,
            low_quote, high_quote, recommended
        )
    
    # Render detailed breakdown and export options
    render_detailed_breakdown(line_items, pdf_callback, excel_callback)

if __name__ == "__main__":
    main() 