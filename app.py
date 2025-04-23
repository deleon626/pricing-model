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
    render_production_form, render_detailed_breakdown, render_rates_editor,
    render_customer_form, render_customer_details, render_customer_quotes,
    render_sidebar_customer_selector, render_customers_table
)
from export_utils import get_table_download_link, generate_pdf_html, get_pdf_download_button
from customer_utils import load_customers, save_customer, get_customer, search_customers, delete_customer
from quote_utils import add_quote, get_quotes_by_customer, get_quote_by_id, update_quote_status, update_quote

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

if "rates" not in st.session_state:
    st.session_state["rates"] = load_rates()

if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = None

if "show_customer_form" not in st.session_state:
    st.session_state.show_customer_form = False

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Quote Builder"

if "confirming_delete_customer_id" not in st.session_state:
    st.session_state.confirming_delete_customer_id = None

# Define tabs globally so it's accessible in the __main__ block
tabs = ["Quote Builder", "Rates"]

def load_rates_json():
    with open("rates.json", "r") as f:
        return json.load(f)

def save_rates_json(rates):
    with open("rates.json", "w") as f:
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
    # --- Customer Management in Sidebar ---
    with st.sidebar:
        st.markdown("## Customer Management")
        # State for table actions
        if "customer_table_action" not in st.session_state:
            st.session_state.customer_table_action = None
        if "customer_table_edit_data" not in st.session_state:
            st.session_state.customer_table_edit_data = None
        customers_data = load_customers().get("customers", [])
        # Customer selector dropdown
        customer_options = [f"{c['name']} ({c['email']})" if c['email'] else c['name'] for c in customers_data]
        customer_id_map = {f"{c['name']} ({c['email']})" if c['email'] else c['name']: c['customer_id'] for c in customers_data}
        selected_label = None
        if st.session_state.selected_customer:
            for label, cid in customer_id_map.items():
                if cid == st.session_state.selected_customer.get("customer_id"):
                    selected_label = label
                    break
        selected_label = st.selectbox(
            "Select Active Customer",
            options=["None"] + customer_options,
            index=(["None"] + customer_options).index(selected_label) if selected_label else 0,
            help="Choose the customer whose data will be used for the questionnaire and production variables."
        )
        if selected_label == "None":
            st.session_state.selected_customer = None
        elif selected_label:
            selected_id = customer_id_map[selected_label]
            if (not st.session_state.selected_customer) or (st.session_state.selected_customer.get("customer_id") != selected_id):
                # Save draft to previous customer before switching
                prev_customer = st.session_state.selected_customer
                if prev_customer:
                    import copy
                    prev_customer_data = get_customer(prev_customer['customer_id'])
                    if prev_customer_data is not None:
                        prev_customer_data['questionnaire_draft'] = copy.deepcopy(st.session_state.questionnaire)
                        prev_customer_data['production_vars_draft'] = copy.deepcopy(st.session_state.production_vars)
                        save_customer(prev_customer_data)
                # Load draft for new customer
                new_customer_data = get_customer(selected_id)
                import copy
                if 'questionnaire_draft' in new_customer_data:
                    st.session_state.questionnaire = copy.deepcopy(new_customer_data['questionnaire_draft'])
                else:
                    st.session_state.questionnaire = DEFAULT_QUESTIONNAIRE.copy()
                if 'production_vars_draft' in new_customer_data:
                    st.session_state.production_vars = copy.deepcopy(new_customer_data['production_vars_draft'])
                else:
                    st.session_state.production_vars = DEFAULT_PRODUCTION_VARS.copy()
                st.session_state.selected_customer = new_customer_data
                st.session_state.show_customer_form = False
                st.session_state.customer_table_action = None
                st.session_state.customer_table_edit_data = None
                st.rerun()
        # Add/Edit/Delete handlers
        def handle_add():
            st.session_state.show_customer_form = True
            st.session_state.selected_customer = None
            st.session_state.customer_table_action = "add"
            st.session_state.customer_table_edit_data = None
        def handle_edit(customer):
            st.session_state.show_customer_form = True
            # Convert pandas Series to dict if needed
            if hasattr(customer, 'to_dict'):
                customer = customer.to_dict()
            st.session_state.selected_customer = customer
            st.session_state.customer_table_action = "edit"
            st.session_state.customer_table_edit_data = customer
        def handle_delete(customer_id):
            print(f"Attempting to delete customer with ID: {customer_id}") # Debug print
            deleted = delete_customer(customer_id)
            print(f"delete_customer returned: {deleted}") # Debug print
            if deleted:
                st.success("Customer deleted.")
                if st.session_state.selected_customer and st.session_state.selected_customer.get("customer_id") == customer_id:
                    st.session_state.selected_customer = None
                st.session_state.show_customer_form = False
                st.session_state.customer_table_action = None
                st.session_state.customer_table_edit_data = None
                st.rerun()
            else:
                st.error("Failed to delete customer.")
        # Show customer form if adding new or editing existing
        if st.session_state.show_customer_form:
            st.subheader("Customer Information Form")
            submitted = render_customer_form(st.session_state.selected_customer)
            if submitted:
                customer_saved = save_customer(st.session_state.customer_form)
                if customer_saved:
                    st.success(f"Customer information saved successfully!")
                    st.session_state.selected_customer = st.session_state.customer_form.copy()
                    st.session_state.show_customer_form = False
                    st.session_state.customer_table_action = None
                    st.session_state.customer_table_edit_data = None
                    st.rerun()
                else:
                    st.error("Failed to save customer information. Please try again.")
        else:
            # Show interactive table
            render_customers_table(
                customers_data,
                on_edit=handle_edit,
                on_delete=handle_delete,
                on_add=handle_add
            )
    # --- Main page content ---
    # Use explicit None check to avoid ambiguous truth value if selected_customer is a Series
    selected_customer = st.session_state.selected_customer
    if isinstance(selected_customer, pd.Series):
        selected_customer = selected_customer.to_dict()
        st.session_state.selected_customer = selected_customer
    render_header("Lapis Visuals - Pricing Calculator" + (f" — {selected_customer['name']}" if selected_customer else ""))
    # --- Quote Builder Tab ---
    if st.session_state.active_tab == "Quote Builder":
        st.header("Client Questionnaire")
        render_questionnaire_form(
            st.session_state.questionnaire,
            DISTRIBUTION_CHANNELS,
            VIDEO_FORMATS,
            SPECIAL_REQUIREMENTS
        )
        render_template_buttons(apply_template)
        st.markdown("---")
        st.header("Production Variables")
        render_production_form(
            st.session_state.production_vars,
            LOCATION_TYPES,
            PROPS_DESIGN_LEVELS,
            FOOTAGE_VOLUME_LEVELS
        )
        
        # Calculate quote and line items
        q = st.session_state.questionnaire
        p = st.session_state.production_vars
        rates = st.session_state.rates
        line_items = generate_line_items(q, p, rates)
        low_quote, high_quote, recommended = calculate_quote(q, p, rates)
        
        st.markdown("---")
        if st.session_state.get("loaded_quote_id"):
            loaded_quote = get_quote_by_id(st.session_state.loaded_quote_id)
            if loaded_quote:
                from ui_components import format_currency
                st.info("**Saved quote amounts reflect rates at the time of saving. Current summary uses latest rates.**")
                comp_data = {
                    "Type": ["Low Estimate", "Recommended", "High Estimate"],
                    "Saved (at time of quote)": [
                        format_currency(loaded_quote.get("low_quote", 0)),
                        format_currency(loaded_quote.get("recommended_quote", 0)),
                        format_currency(loaded_quote.get("high_quote", 0)),
                    ],
                    "Live (current rates)": [
                        format_currency(low_quote),
                        format_currency(recommended),
                        format_currency(high_quote),
                    ],
                }
                st.table(pd.DataFrame(comp_data))
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
        st.markdown("---")
        st.subheader("Quote Actions")
        save_col, clear_col, _ = st.columns([1, 1, 2])
        with save_col:
            if st.session_state.get("loaded_quote_id"):
                if st.button("🔄 Update Quote", disabled=not st.session_state.selected_customer):
                    if st.session_state.selected_customer:
                        customer_id = st.session_state.selected_customer['customer_id']
                        project_name = st.session_state.questionnaire.get("project_name", "Untitled Project")
                        updates = {
                            "customer_id": customer_id,
                            "project_name": project_name,
                            "questionnaire_snapshot": st.session_state.questionnaire,
                            "production_vars_snapshot": st.session_state.production_vars,
                            "low_quote": low_quote,
                            "high_quote": high_quote,
                            "recommended_quote": recommended,
                            "line_items_snapshot": line_items
                        }
                        updated = update_quote(st.session_state.loaded_quote_id, updates)
                        if updated:
                            st.success(f"Quote '{st.session_state.loaded_quote_id}' updated for {st.session_state.selected_customer['name']}!")
                            st.session_state.loaded_quote_id = None
                        else:
                            st.error("Failed to update quote. Please try again.")
                    else:
                        st.warning("Please select a customer before updating a quote.")
            else:
                if st.button("💾 Save Current Quote", disabled=not st.session_state.selected_customer):
                    if st.session_state.selected_customer:
                        customer_id = st.session_state.selected_customer['customer_id']
                        project_name = st.session_state.questionnaire.get("project_name", "Untitled Project")
                        new_quote = add_quote(customer_id, project_name, st.session_state.questionnaire, st.session_state.production_vars, low_quote, high_quote, recommended, line_items)
                    else:
                        st.warning("Please select a customer before saving a quote.")
        with clear_col:
            if st.session_state.get("loaded_quote_id"):
                if st.button("❌ Clear Loaded Quote"):
                    st.session_state.loaded_quote_id = None
                    st.success("Loaded quote cleared. You can now start a new quote.")
        render_detailed_breakdown(line_items, pdf_callback, excel_callback)
    # --- Rates Tab ---
    elif st.session_state.active_tab == "Rates":
        st.header("Rate Card Editor")
        submitted = render_rates_editor(rates)
        if submitted:
            save_rates_json(rates)
            st.success("Rates updated!")
            st.rerun()

if __name__ == "__main__":
    # Render tabs selector at the top
    # Check if active_tab is already set, otherwise default to first tab
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = tabs[0]
        
    selected_tab = st.radio(
        "Navigation",
        options=tabs, # Now uses the global 'tabs' list
        index=tabs.index(st.session_state.active_tab), # Set index based on current state
        key="main_tabs",
        horizontal=True,
        label_visibility="collapsed"
    )
    # Update the session state only if the selected tab changes
    if selected_tab != st.session_state.active_tab:
        st.session_state.active_tab = selected_tab
        st.rerun() # Rerun if the tab selection changes
    
    main() # Run the main function which now conditionally renders based on active_tab 