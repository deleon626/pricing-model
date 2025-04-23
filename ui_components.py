"""
Reusable UI components for the Lapis Visuals Pricing Calculator.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Tuple, Callable
from datetime import datetime
import pytz # Import pytz for timezone handling

# Import quote utils for status update
from quote_utils import update_quote_status

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
                              special_requirements_options: List[str]) -> None:
    """
    Render the client questionnaire form using live widgets (no form, no submit button).
    Updates the questionnaire dict in place.
    """
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
    # No return, as everything is live-updated

def render_production_form(production_vars: Dict[str, Any],
                          location_options: List[str],
                          props_design_options: List[str],
                          footage_volume_options: List[str]) -> None:
    """
    Render the production variables form using live widgets (no form, no submit button).
    Updates the production_vars dict in place.
    """
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
    # No return, as everything is live-updated

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

def render_customer_form(customer=None):
    """
    Render a form for collecting customer information
    
    Args:
        customer: Optional existing customer data to pre-fill the form
    
    Returns:
        Boolean indicating if form was submitted
    """
    if customer is None:
        # Default empty customer template
        customer = {
            "customer_id": "",
            "name": "",
            "email": "",
            "phone": "",
            "company": "",
            "address": {
                "street": "",
                "city": "",
                "state": "",
                "postal_code": "",
                "country": ""
            },
            "preferences": {
                "communication": "email",
                "newsletter": False
            },
            "notes": ""
        }
    
    # Initialize session state for form data if not exists
    if "customer_form" not in st.session_state:
        st.session_state.customer_form = customer.copy()
    
    with st.form("customer_information_form"):
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.customer_form["name"] = st.text_input(
                "Full Name", 
                value=st.session_state.customer_form.get("name", "")
            )
            st.session_state.customer_form["email"] = st.text_input(
                "Email", 
                value=st.session_state.customer_form.get("email", "")
            )
        
        with col2:
            st.session_state.customer_form["phone"] = st.text_input(
                "Phone", 
                value=st.session_state.customer_form.get("phone", "")
            )
            st.session_state.customer_form["company"] = st.text_input(
                "Company", 
                value=st.session_state.customer_form.get("company", "")
            )
        
        st.subheader("Address")
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.customer_form["address"]["street"] = st.text_input(
                "Street Address", 
                value=st.session_state.customer_form["address"].get("street", "")
            )
            st.session_state.customer_form["address"]["city"] = st.text_input(
                "City", 
                value=st.session_state.customer_form["address"].get("city", "")
            )
        
        with col2:
            st.session_state.customer_form["address"]["state"] = st.text_input(
                "State/Province", 
                value=st.session_state.customer_form["address"].get("state", "")
            )
            st.session_state.customer_form["address"]["postal_code"] = st.text_input(
                "Postal Code", 
                value=st.session_state.customer_form["address"].get("postal_code", "")
            )
            st.session_state.customer_form["address"]["country"] = st.text_input(
                "Country", 
                value=st.session_state.customer_form["address"].get("country", "")
            )
        
        st.subheader("Preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            comm_options = ["email", "phone", "both"]
            st.session_state.customer_form["preferences"]["communication"] = st.selectbox(
                "Preferred Communication", 
                options=comm_options,
                index=comm_options.index(st.session_state.customer_form["preferences"].get("communication", "email"))
            )
        
        with col2:
            st.session_state.customer_form["preferences"]["newsletter"] = st.checkbox(
                "Subscribe to Newsletter", 
                value=st.session_state.customer_form["preferences"].get("newsletter", False)
            )
        
        st.session_state.customer_form["notes"] = st.text_area(
            "Additional Notes", 
            value=st.session_state.customer_form.get("notes", "")
        )
        
        submitted = st.form_submit_button("Save Customer Information")
        name_error = False
        if submitted:
            # Validate name is not empty
            if not st.session_state.customer_form["name"].strip():
                st.error("Full Name is required.")
                name_error = True
            # Generate a customer_id if not present and name is valid
            if not name_error:
                if not st.session_state.customer_form.get("customer_id"):
                    import uuid
                    import time
                    st.session_state.customer_form["customer_id"] = f"CUST{int(time.time())}-{str(uuid.uuid4())[:8]}"
                return True
        return False

def render_customer_details(customer):
    """
    Render detailed customer information including project history
    
    Args:
        customer: Customer data to display
    """
    if not customer:
        st.warning("No customer selected")
        return
    
    # Basic customer info
    st.subheader(f"{customer['name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**ID:** {customer['customer_id']}")
        st.write(f"**Email:** {customer['email']}")
        st.write(f"**Phone:** {customer['phone']}")
    
    with col2:
        st.write(f"**Company:** {customer['company']}")
        st.write(f"**Communication Preference:** {customer['preferences']['communication']}")
        newsletter = "Yes" if customer['preferences'].get('newsletter', False) else "No"
        st.write(f"**Newsletter:** {newsletter}")
    
    # Address
    with st.expander("Address Details"):
        addr = customer.get('address', {})
        st.write(f"{addr.get('street', '')}")
        st.write(f"{addr.get('city', '')}, {addr.get('state', '')} {addr.get('postal_code', '')}")
        st.write(f"{addr.get('country', '')}")
    
    # Notes
    if customer.get('notes'):
        with st.expander("Notes"):
            st.write(customer['notes'])
    
    # Project History
    st.subheader("Project History")
    
    if customer.get('project_history') and len(customer['project_history']) > 0:
        # Convert project history to a DataFrame for display
        projects_df = pd.DataFrame(customer['project_history'])
        
        # Format currency
        if 'quote_amount' in projects_df.columns:
            projects_df['quote_amount'] = projects_df['quote_amount'].apply(
                lambda x: f"Rp {'{:,.0f}'.format(x).replace(',', '.')}" if x else "N/A"
            )
        
        # Reorder and rename columns for display
        cols_order = ['project_id', 'project_name', 'date', 'status', 'quote_amount']
        cols_display = {
            'project_id': 'ID',
            'project_name': 'Project Name',
            'date': 'Date',
            'status': 'Status',
            'quote_amount': 'Quote Amount'
        }
        
        # Select only columns that exist
        display_cols = [col for col in cols_order if col in projects_df.columns]
        
        # Rename and display
        st.dataframe(
            projects_df[display_cols].rename(columns={
                col: cols_display.get(col, col) for col in display_cols
            }),
            use_container_width=True
        )
    else:
        st.info("No project history available for this customer.")

def render_customer_quotes(quotes: List[Dict[str, Any]]) -> str | None:
    """
    Renders the list of quotes for a customer, allowing status updates and loading.
    Returns the quote_id if the 'Load Quote' button is pressed, otherwise None.
    """
    if not quotes:
        st.info("No quotes found for this customer.")
        return None
    
    selected_quote_to_load = None
    
    # Define possible statuses
    QUOTE_STATUSES = ["Draft", "Quoted", "Approved", "Rejected", "Invoiced", "Paid", "Archived"]
    
    # Prepare data for display (convert datetime for display)
    display_data = []
    for quote in quotes:
        # Ensure creation_date is timezone-aware before converting
        creation_dt = quote.get('creation_date')
        if isinstance(creation_dt, str): # Handle potential string dates from JSON
            try:
                creation_dt = datetime.fromisoformat(creation_dt)
            except ValueError:
                creation_dt = None # Or handle error appropriately
        
        # Assume UTC if naive, or convert to a common timezone like UTC
        # This part might need adjustment based on how dates are stored
        if creation_dt and creation_dt.tzinfo is None:
             # Assuming dates are stored in local time or UTC - let's assume UTC for consistency
             creation_dt = pytz.utc.localize(creation_dt)
        
        # Convert to a readable local time (e.g., Jakarta time)
        try:
            jakarta_tz = pytz.timezone('Asia/Jakarta')
            local_creation_date = creation_dt.astimezone(jakarta_tz).strftime("%Y-%m-%d %H:%M") if creation_dt else "N/A"
        except Exception as e:
            # Fallback if timezone conversion fails
            local_creation_date = creation_dt.strftime("%Y-%m-%d %H:%M") if creation_dt else "N/A"
            st.warning(f"Timezone conversion issue: {e}")

        display_data.append({
            "ID": quote.get('quote_id', 'N/A'),
            "Project Name": quote.get('project_name', 'N/A'),
            "Date Created": local_creation_date,
            "Status": quote.get('status', 'N/A'),
            "Amount (Recommended)": format_currency(quote.get('recommended_quote', 0)),
            "_quote_obj": quote # Keep original object for actions
        })
        
    # Display quotes using columns for layout
    st.markdown("#### Quotes List")
    cols = st.columns((1, 2, 1.5, 1.5, 1.5, 1)) # Adjust ratios as needed
    headers = ["ID", "Project Name", "Date Created", "Status", "Amount", "Actions"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    for item in display_data:
        quote_id = item["ID"]
        quote_obj = item["_quote_obj"]
        current_status = item["Status"]
        
        col1, col2, col3, col4, col5, col6 = st.columns((1, 2, 1.5, 1.5, 1.5, 1))
        
        with col1:
            st.write(item["ID"])
        with col2:
            st.write(item["Project Name"])
        with col3:
            st.write(item["Date Created"])
        with col4:
            # Use a unique key for each selectbox based on quote_id
            status_key = f"status_select_{quote_id}"
            try:
                current_index = QUOTE_STATUSES.index(current_status)
            except ValueError:
                current_index = 0 # Default to first status if current is invalid
            
            new_status = st.selectbox(
                "Status", 
                options=QUOTE_STATUSES, 
                index=current_index, 
                key=status_key, 
                label_visibility="collapsed"
            )
            # Check if status changed and update if needed
            if new_status != current_status:
                if update_quote_status(quote_id, new_status):
                    st.success(f"Status for {quote_id} updated to {new_status}")
                    st.rerun() # Rerun to reflect the status change immediately
                else:
                    st.error(f"Failed to update status for {quote_id}")
                    
        with col5:
            st.write(item["Amount (Recommended)"])
        with col6:
            # Use a unique key for each button
            load_key = f"load_button_{quote_id}"
            if st.button("Load", key=load_key):
                selected_quote_to_load = quote_id
                
    return selected_quote_to_load 

def render_sidebar_customer_selector(selected_customer, show_customer_form, DEFAULT_QUESTIONNAIRE, DEFAULT_PRODUCTION_VARS, search_customers, save_customer, get_customer):
    """
    Render the customer search/select/add UI in the sidebar.
    Returns (new_selected_customer, show_customer_form, action)
    action: 'edit', 'add', or None
    """
    # Search box
    search_query = st.sidebar.text_input("Search Customers (name, email, or company)", key="sidebar_customer_search")
    newly_selected_customer = None
    action = None
    results = []
    if search_query:
        results = search_customers(search_query)
        if results:
            options = ["Select a customer..."] + [f"{c['name']} ({c['email']})" for c in results]
            selected_option = st.sidebar.selectbox("Search Results", options, key="sidebar_customer_select")
            if selected_option != "Select a customer...":
                newly_selected_customer = results[options.index(selected_option) - 1]
                show_customer_form = False
        else:
            st.sidebar.info("No customers found matching your search.")
    # Add New Customer button
    if st.sidebar.button("Add New Customer", key="sidebar_add_customer"):
        # Save current draft to previous customer before clearing
        prev_customer = selected_customer
        if prev_customer and not show_customer_form:
            prev_customer_data = get_customer(prev_customer['customer_id'])
            if prev_customer_data is not None:
                prev_customer_data['questionnaire_draft'] = st.session_state.questionnaire.copy()
                prev_customer_data['production_vars_draft'] = st.session_state.production_vars.copy()
                save_customer(prev_customer_data)
        show_customer_form = True
        newly_selected_customer = None
        st.session_state.questionnaire = DEFAULT_QUESTIONNAIRE.copy()
        st.session_state.production_vars = DEFAULT_PRODUCTION_VARS.copy()
        action = 'add'
    # Edit Customer button
    if selected_customer and not show_customer_form:
        if st.sidebar.button("Edit Customer", key="sidebar_edit_customer"):
            show_customer_form = True
            action = 'edit'
    return newly_selected_customer, show_customer_form, action 

def render_customers_table(customers: List[Dict[str, Any]], on_edit: Callable, on_delete: Callable, on_add: Callable):
    """
    Render an interactive table for customers with Edit/Delete actions.
    Includes inline confirmation for deletion.
    """
    st.subheader("Manage Customers")

    # Initialize confirming_delete_customer_id if not present (safety check)
    if 'confirming_delete_customer_id' not in st.session_state:
        st.session_state.confirming_delete_customer_id = None

    if not customers:
        st.info("No customers found. Add one to get started.")
        if st.button("➕ Add First Customer"):
            on_add()
        return

    # Prepare data for display (including placeholders for actions)
    display_data = []
    for customer in customers:
        # Ensure consistent structure, handle potential missing keys gracefully
        row_data = {
            'customer_id': customer.get('customer_id', 'N/A'),
            'Name': customer.get('name', 'N/A'),
            'Email': customer.get('email', ''),
            'Company': customer.get('company', ''),
            'Added': customer.get('created_at', 'N/A') # Assuming created_at exists
        }
        # Format timestamp if it exists and is a valid format
        if 'created_at' in customer and customer['created_at']:
            try:
                # Assuming created_at is a Unix timestamp or ISO string
                ts = pd.to_datetime(customer['created_at'])
                row_data['Added'] = ts.strftime('%Y-%m-%d') # Just date for brevity
            except (ValueError, TypeError):
                 row_data['Added'] = 'Invalid Date' # Handle parsing errors


        display_data.append(row_data)

    df = pd.DataFrame(display_data)

    # Display basic info table (consider using st.dataframe with configuration for actions later)
    # Simplified for clarity - Using columns for button layout
    st.markdown("---")
    cols = st.columns([2, 3, 2, 2, 3]) # Adjust widths as needed: Name, Email, Company, Added, Actions
    headers = ["Name", "Email", "Company", "Added", "Actions"]
    for col, header in zip(cols, headers):
        col.markdown(f"**{header}**")

    for index, row in df.iterrows():
        customer_id = row['customer_id']
        col1, col2, col3, col4, col5 = st.columns([2, 3, 2, 2, 3])

        with col1:
            st.write(row['Name'])
        with col2:
            st.write(row['Email'] or "-")
        with col3:
            st.write(row['Company'] or "-")
        with col4:
            st.write(row['Added'])
        with col5:
            # Remove nested columns: action_col1, action_col2 = st.columns(2)
            customer_data_for_edit = next((c for c in customers if c.get('customer_id') == customer_id), None)

            # Edit Button (place directly in col5)
            edit_button_placeholder = st.empty() # Use placeholder if needed for dynamic visibility
            if not (st.session_state.confirming_delete_customer_id == customer_id): # Hide edit when confirming delete
                if edit_button_placeholder.button("✏️", key=f"edit_{customer_id}", help="Edit Customer"):
                    if customer_data_for_edit:
                        on_edit(customer_data_for_edit)
                    else:
                        st.error(f"Could not find full data for customer ID {customer_id}")

            # Delete/Confirm/Cancel Buttons (place directly in col5)
            delete_button_placeholder = st.empty()
            confirm_button_placeholder = st.empty()
            cancel_button_placeholder = st.empty()

            if st.session_state.confirming_delete_customer_id == customer_id:
                # Show Confirm/Cancel buttons
                if confirm_button_placeholder.button("✔️", key=f"confirm_{customer_id}", help="Confirm Delete"):
                    on_delete(customer_id)
                    st.session_state.confirming_delete_customer_id = None
                    st.rerun()
                if cancel_button_placeholder.button("❌", key=f"cancel_{customer_id}", help="Cancel Delete"):
                    st.session_state.confirming_delete_customer_id = None
                    st.rerun()
            else:
                # Show standard Delete button
                if delete_button_placeholder.button("🗑️", key=f"delete_{customer_id}", help="Delete Customer"):
                    st.session_state.confirming_delete_customer_id = customer_id
                    st.rerun()

    st.markdown("---")
    if st.button("➕ Add New Customer"):
        on_add() 