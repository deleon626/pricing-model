# Lapis Visuals - Project Pricing Calculator

A Streamlit-based calculator that converts client briefs into defensible cost estimates for video productions.

## Features

- **Client Questionnaire**: Capture all project requirements
- **Production Variables**: Configure internal production settings
- **Real-time Pricing**: See cost estimates update in real-time
- **Templates**: Load preset configurations for common project types
- **Detailed Breakdown**: Itemized cost breakdown with low and high estimates
- **Export Options**: Save quotes as PDF or Excel
- **Rate Card Editor**: Update pricing information directly in the application
- **Customer Management**: Store and manage customer information and link quotes to customers

## Setup & Installation

1. Make sure you have Python 3.8+ installed
2. Clone this repository
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage

1. Fill out the Client Questionnaire form
2. Adjust Production Variables as needed
3. View the real-time quote in the sidebar
4. Navigate to the Quote Summary for a detailed breakdown
5. Use the template buttons to quickly load preset configurations
6. Edit rates directly in the app when needed
7. Add and manage customers in the Customer Management tab
8. Link quotes to customer records for future reference

## Project Structure

- `app.py` - Main Streamlit application
- `constants.py` - Default values and configuration constants
- `pricing_logic.py` - Functions for calculating quotes and line items
- `templates.py` - Preset project configurations
- `ui_components.py` - Modular UI components
- `export_utils.py` - PDF and Excel export functionality
- `customer_utils.py` - Customer data management functions
- `rates.json` - Configuration file for pricing rates
- `customers.json` - Customer database
- `requirements.txt` - Python dependencies

## Notes

- Format currency in Rupiah with dot separators (e.g., Rp 5.000.000)
- Projects under Rp 20M exclude admin/overhead costs
- User roles can be selected from the sidebar
- Customer data is stored locally in customers.json

## Future Enhancements

- Integration with accounting systems (Xero)
- Project management integration
- CRM integration for quote history
- Analytics dashboard for pricing trends
- Multi-currency support 