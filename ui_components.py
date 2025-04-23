"""
Reusable UI components for the Lapis Visuals Pricing Calculator.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Tuple, Callable

def render_header(title: str, subheader: str = None):
    """Render a consistent header."""
    st.title(title)
    if subheader:
        st.subheader(subheader)
    st.markdown("---")

def render_sidebar_user_role() -> str:
    """Render the user role selector in sidebar and return the selected role."""
    st.sidebar.title("Lapis Visuals")
    st.sidebar.subheader("Pricing Calculator")
    user_role = st.sidebar.selectbox(
        "Select Role:",
        ["Account Manager", "Producer / PM", "Finance", "Client"]
    )
    st.sidebar.markdown("---")
    st.sidebar.info(f"Version: 1.0.0 | User: {user_role}")
    return user_role

def render_sidebar_quote_summary(low_quote: int, high_quote: int, recommended: int, mini_items: Dict[str, Dict[str, float]]):
    """Render the quote summary in the sidebar."""
    st.sidebar.markdown("## Quote Summary")
    st.sidebar.metric("Low Estimate", f"Rp {low_quote:,.0f}".replace(",", "."))
    st.sidebar.metric("Recommended", f"Rp {recommended:,.0f}".replace(",", "."))
    st.sidebar.metric("High Estimate", f"Rp {high_quote:,.0f}".replace(",", "."))
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Mini Breakdown**")
    
    # Convert items to DataFrame for display
    mini_df = pd.DataFrame(mini_items).T.reset_index()
    mini_df.columns = ["Item", "Low (Rp)", "High (Rp)"]
    mini_df["Low (Rp)"] = mini_df["Low (Rp)"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
    mini_df["High (Rp)"] = mini_df["High (Rp)"].apply(lambda x: f"Rp {x:,.0f}".replace(",", "."))
    st.sidebar.dataframe(mini_df, hide_index=True, use_container_width=True)

def format_currency(value: float) -> str:
    """Format a value as Indonesian Rupiah."""
    return f"Rp {value:,.0f}".replace(",", ".")

def render_number_input(label: str, key: str, min_value: float, max_value: float, 
                        value: float, step: float = 1.0, help_text: str = None,
                        is_float: bool = True, format_str: str = None) -> float:
    """Render a standardized number input field."""
    if is_float:
        result = st.number_input(
            label,
            min_value=float(min_value),
            max_value=float(max_value),
            value=float(value),
            step=float(step),
            help=help_text
        )
    else:
        result = st.number_input(
            label,
            min_value=int(min_value),
            max_value=int(max_value),
            value=int(value),
            step=int(step),
            format=format_str,
            help=help_text
        )
    return result

def render_rate_card(rates: Dict[str, Any]):
    """Render the rate card in an expander."""
    with st.expander("View Current Rate Card", expanded=False):
        st.header("Current Rate Card")

        # Scriptwriting
        st.subheader("Scriptwriting")
        st.write(f"Base: {format_currency(rates['scriptwriting']['base'])}")
        st.write("Complexity Factors:")
        st.table(pd.DataFrame(list(rates['scriptwriting']['complexity_factors'].items()), 
                             columns=["Level", "Multiplier"]))

        # Storyboard
        st.subheader("Storyboard")
        st.write(f"Base: {format_currency(rates['storyboard']['base'])}")

        # Location
        st.subheader("Location")
        location_df = pd.DataFrame(list(rates['location'].items()), columns=["Type", "Cost (Rp)"])
        location_df["Cost (Rp)"] = location_df["Cost (Rp)"].apply(lambda x: format_currency(x) if x > 0 else "0")
        st.table(location_df)

        # Crew Roles
        st.subheader("Crew Roles")
        crew_df = pd.DataFrame(list(rates['crew_roles'].items()), columns=["Role", "Rate (Rp)"])
        crew_df["Rate (Rp)"] = crew_df["Rate (Rp)"].apply(format_currency)
        st.table(crew_df)

        # Equipment
        st.subheader("Equipment")
        equipment_df = pd.DataFrame(list(rates['equipment'].items()), columns=["Tier", "Daily Rate (Rp)"])
        equipment_df["Daily Rate (Rp)"] = equipment_df["Daily Rate (Rp)"].apply(format_currency)
        st.table(equipment_df)

        # Post Production
        st.subheader("Post Production")
        for key, val in rates['post_production'].items():
            st.markdown(f"**{key.capitalize()}**")
            st.write(f"Per Minute: {format_currency(val['per_minute'])}")
            st.write("Complexity Multipliers:")
            st.table(pd.DataFrame(list(val['complexity'].items()), columns=["Level", "Multiplier"]))

        # Producer Fee
        st.subheader("Producer Fee")
        st.write(f"Percent: {rates['producer_fee']['percent']*100:.1f}%")

        # Contingency
        st.subheader("Contingency")
        st.write(f"Default: {int(rates['contingency']['default']*100)}%")

def render_rates_editor(rates: Dict[str, Any]) -> bool:
    """
    Render a form to edit the rates dictionary. Returns True if the form was submitted.
    """
    with st.expander("Edit Rates (Admin Only)"):
        st.info("Edit the rates below and click 'Save Rates' to update. Changes affect all users.")
        updated_rates = {}
        with st.form("edit_rates_form"):
            # Scriptwriting
            st.subheader("Scriptwriting")
            updated_rates["scriptwriting"] = {}
            updated_rates["scriptwriting"]["base"] = st.number_input(
                "Scriptwriting Base", value=rates["scriptwriting"]["base"], step=100000
            )
            updated_rates["scriptwriting"]["complexity_factors"] = {}
            for k, v in rates["scriptwriting"]["complexity_factors"].items():
                updated_rates["scriptwriting"]["complexity_factors"][k] = st.number_input(
                    f"Scriptwriting Complexity - {k}", value=float(v), step=0.1, format="%.2f"
                )

            # Storyboard
            st.subheader("Storyboard")
            updated_rates["storyboard"] = {}
            updated_rates["storyboard"]["base"] = st.number_input(
                "Storyboard Base", value=rates["storyboard"]["base"], step=100000
            )

            # Location
            st.subheader("Location")
            updated_rates["location"] = {}
            for k, v in rates["location"].items():
                updated_rates["location"][k] = st.number_input(
                    f"Location - {k}", value=int(v), step=500000
                )

            # Crew Roles
            st.subheader("Crew Roles")
            updated_rates["crew_roles"] = {}
            for k, v in rates["crew_roles"].items():
                updated_rates["crew_roles"][k] = st.number_input(
                    f"Crew Role - {k}", value=int(v), step=500000
                )

            # Equipment
            st.subheader("Equipment")
            updated_rates["equipment"] = {}
            for k, v in rates["equipment"].items():
                updated_rates["equipment"][k] = st.number_input(
                    f"Equipment - {k}", value=int(v), step=500000
                )

            # Post Production
            st.subheader("Post Production")
            updated_rates["post_production"] = {}
            for section, section_val in rates["post_production"].items():
                updated_rates["post_production"][section] = {}
                updated_rates["post_production"][section]["per_minute"] = st.number_input(
                    f"{section.capitalize()} Per Minute", value=int(section_val["per_minute"]), step=100000
                )
                updated_rates["post_production"][section]["complexity"] = {}
                for k, v in section_val["complexity"].items():
                    updated_rates["post_production"][section]["complexity"][k] = st.number_input(
                        f"{section.capitalize()} Complexity - {k}", value=float(v), step=0.1, format="%.2f"
                    )

            # Producer Fee
            st.subheader("Producer Fee")
            updated_rates["producer_fee"] = {}
            updated_rates["producer_fee"]["percent"] = st.number_input(
                "Producer Fee Percent", value=float(rates["producer_fee"]["percent"]), step=0.01, format="%.3f"
            )

            # Contingency
            st.subheader("Contingency")
            updated_rates["contingency"] = {}
            updated_rates["contingency"]["default"] = st.number_input(
                "Contingency Default", value=float(rates["contingency"]["default"]), step=0.01, format="%.2f"
            )

            submitted = st.form_submit_button("Save Rates")
            if submitted:
                st.success("Rates updated! Please refresh or rerun the app.")
            return submitted

def render_template_buttons(callback: Callable):
    """Render template selection buttons."""
    st.markdown("### Load Template")
    template_cols = st.columns(4)
    with template_cols[0]:
        if st.button("Commercial"):
            callback("commercial")
    with template_cols[1]:
        if st.button("Social Snippet"):
            callback("social")
    with template_cols[2]:
        if st.button("Documentary"):
            callback("documentary")
    with template_cols[3]:
        if st.button("Event Coverage"):
            callback("event")

def render_questionnaire_form(questionnaire: Dict[str, Any], 
                              distribution_options: List[str],
                              format_options: List[str],
                              special_requirements_options: List[str]) -> bool:
    """
    Render the client questionnaire form.
    
    Returns:
        bool: True if form was submitted, False otherwise
    """
    with st.form("client_form"):
        col1, col2 = st.columns(2)
        with col1:
            # Video length
            questionnaire["video_length"] = render_number_input(
                "Final Video Length (minutes)",
                "video_length",
                0.5, 30.0, questionnaire["video_length"],
                step=0.5,
                help_text="The total duration of the finished video in minutes. Directly increases post-production costs and influences the scale of the project."
            )
            
            # Deliverables
            questionnaire["deliverables"] = render_number_input(
                "Number of Deliverables",
                "deliverables",
                1, 20, questionnaire["deliverables"],
                is_float=False,
                help_text="The number of separate video outputs required (e.g., main video plus cutdowns). Increases pre-production (storyboard) and may affect overall workload."
            )
            
            # Distribution channels
            questionnaire["distribution"] = st.multiselect(
                "Distribution Channel(s)",
                distribution_options,
                default=questionnaire["distribution"],
                help="Where the video will be published (e.g., Instagram, YouTube). May influence format, complexity, and deliverable count, but not directly priced in current logic."
            )
            
            # Format/Genre
            questionnaire["format"] = st.selectbox(
                "Format / Genre",
                format_options,
                index=0 if not questionnaire["format"] else format_options.index(questionnaire["format"]),
                help="The style or type of video (e.g., Commercial, Documentary). Sets expectations for complexity and may affect template defaults."
            )
        with col2:
            # Special requirements
            questionnaire["special_requirements"] = st.multiselect(
                "Special Requirements",
                special_requirements_options,
                default=questionnaire["special_requirements"],
                help="Any advanced production needs (e.g., SFX, Motion Graphics, Green Screen, Aerial Shots, Underwater). Each selected item increases the complexity factor, raising the overall quote."
            )
            
            # Concept summary
            questionnaire["concept"] = st.text_area(
                "Concept Summary",
                value=questionnaire["concept"],
                height=100,
                help="A brief description of the video's creative idea. For reference only; does not affect calculation."
            )
            
            # Dates
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                questionnaire["shoot_date"] = st.date_input(
                    "Ideal Shoot Date",
                    value=questionnaire["shoot_date"],
                    help="Preferred date for filming. For scheduling only; does not affect calculation."
                )
            with col_date2:
                questionnaire["delivery_date"] = st.date_input(
                    "Final Delivery Date",
                    value=questionnaire["delivery_date"],
                    help="Preferred date for delivery. For scheduling only; does not affect calculation."
                )
            
            # Budget range
            st.markdown("#### Budget Range (optional)")
            budget_cols = st.columns(2)
            with budget_cols[0]:
                questionnaire["budget_min"] = render_number_input(
                    "Minimum (Rp)",
                    "budget_min",
                    0, 1000000000, 
                    int(questionnaire["budget_min"]) if questionnaire["budget_min"] else 0,
                    step=1000000,
                    is_float=False,
                    format_str="%d",
                    help_text="Client's minimum budget. For reference only; does not affect calculation."
                )
            with budget_cols[1]:
                questionnaire["budget_max"] = render_number_input(
                    "Maximum (Rp)",
                    "budget_max",
                    0, 1000000000, 
                    int(questionnaire["budget_max"]) if questionnaire["budget_max"] else 0,
                    step=1000000,
                    is_float=False,
                    format_str="%d",
                    help_text="Client's maximum budget. For reference only; does not affect calculation."
                )
                
        submit_questionnaire = st.form_submit_button("Save Questionnaire")
        if submit_questionnaire:
            st.success("Questionnaire saved!")
        
        return submit_questionnaire

def render_production_form(production_vars: Dict[str, Any],
                          location_options: List[str],
                          props_design_options: List[str],
                          footage_volume_options: List[str]) -> bool:
    """
    Render the production variables form.
    
    Returns:
        bool: True if form was submitted, False otherwise
    """
    with st.form("production_form"):
        col1, col2 = st.columns(2)
        with col1:
            # Shooting days
            production_vars["shooting_days"] = render_number_input(
                "Shooting Days",
                "shooting_days",
                0.5, 14.0, production_vars["shooting_days"],
                step=0.5,
                help_text="Number of days required for filming. Multiplies crew, equipment, and some location costs."
            )
            
            # Crew size
            production_vars["crew_size"] = render_number_input(
                "Crew Size",
                "crew_size",
                1, 20, production_vars["crew_size"],
                is_float=False,
                help_text="Number of crew members needed. Increases crew costs (each role has a set rate)."
            )
            
            # Location type
            production_vars["location"] = st.selectbox(
                "Location Type",
                location_options,
                index=location_options.index(production_vars["location"]),
                help="The type of location for the shoot (e.g., Studio, Styled Home). Adds a fixed cost based on the selected location."
            )
        with col2:
            # Talent count and agency markup
            talent_col1, talent_col2 = st.columns([3, 1])
            with talent_col1:
                production_vars["talent_count"] = render_number_input(
                    "Talent Count",
                    "talent_count",
                    0, 20, production_vars["talent_count"],
                    is_float=False,
                    help_text="Number of on-screen talents/actors. Increases talent costs; higher if agency markup is selected."
                )
            with talent_col2:
                production_vars["agency_markup"] = st.checkbox(
                    "Agency Markup",
                    value=production_vars["agency_markup"],
                    help="Whether an agency is involved in talent sourcing. Increases talent costs by a markup factor."
                )
            
            # Props and set design
            production_vars["props_design"] = st.selectbox(
                "Props & Set Design",
                props_design_options,
                index=props_design_options.index(production_vars["props_design"]),
                help="The level of set and prop customization (Basic, Custom, Elaborate). Sets a fixed cost for props and set design."
            )
            
            # Footage volume
            production_vars["footage_volume"] = st.selectbox(
                "Footage Volume",
                footage_volume_options,
                index=footage_volume_options.index(production_vars["footage_volume"]),
                help="The expected amount of footage to be shot (Low, Standard, High). Adjusts post-production editing costs (higher volume = higher cost)."
            )
            
            # Contingency
            production_vars["contingency"] = st.slider(
                "Contingency %",
                min_value=0,
                max_value=20,
                value=int(production_vars["contingency"]),
                help="Extra percentage added to cover unforeseen costs. Adds a percentage of the subtotal to the final quote."
            )
            
        submit_production = st.form_submit_button("Save Production Variables")
        if submit_production:
            st.success("Production variables saved!")
            
        return submit_production

def render_detailed_breakdown(line_items: Dict[str, Dict[str, float]], pdf_callback: Callable, excel_callback: Callable):
    """Render the detailed quote breakdown and export options."""
    st.header("Detailed Breakdown & Export")
    
    # Convert line items to DataFrame
    df = pd.DataFrame(line_items).T.reset_index()
    df.columns = ["Item", "Low (Rp)", "High (Rp)"]
    df["Low (Rp)"] = df["Low (Rp)"].apply(lambda x: format_currency(x))
    df["High (Rp)"] = df["High (Rp)"].apply(lambda x: format_currency(x))
    
    # Display table
    st.table(df)
    
    # Export options
    export_col1, export_col2 = st.columns(2)
    with export_col1:
        if st.button("Export to PDF"):
            pdf_callback()
    with export_col2:
        excel_link = excel_callback()
        st.markdown(excel_link, unsafe_allow_html=True) 