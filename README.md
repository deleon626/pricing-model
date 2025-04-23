# Lapis Visuals - Project Pricing Calculator

A Streamlit-based calculator that converts client briefs into defensible cost estimates for video productions.

## Features

- **Client Questionnaire**: Capture all project requirements
- **Production Variables**: Configure internal production settings
- **Real-time Pricing**: See cost estimates update in real-time
- **Templates**: Load preset configurations for common project types
- **Detailed Breakdown**: Itemized cost breakdown with low and high estimates
- **Export Options**: Save quotes as PDF or Excel (placeholder in current version)

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

## Customization

Edit the `rates.json` file to update pricing information without modifying the code.

## Project Structure

- `app.py` - Main Streamlit application
- `rates.json` - Configuration file for pricing rates
- `requirements.txt` - Python dependencies

## Notes

- This is the initial scaffold version
- PDF and Excel export functionality placeholders only
- Format currency in Rupiah with dot separators (e.g., Rp 5.000.000)
- Projects under Rp 20M exclude admin/overhead costs

## Future Enhancements

- Integration with accounting systems (Xero)
- Project management integration
- CRM integration for quote history
- Analytics dashboard for pricing trends
- Multi-currency support 