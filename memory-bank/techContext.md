# Tech Context

## Technologies Used
- Python 3.x
- Streamlit (for UI)
- JSON (for data storage)
- UUID (for customer ID generation)

## Development Setup
- Local development with virtual environments (see .venv/)
- Requirements managed via requirements.txt
- Run the app with Streamlit CLI (e.g., `streamlit run app.py`)

## Technical Constraints
- Must remain compatible with Streamlit and Python 3.x
- Data must be easily exportable/importable (JSON, CSV)
- UI should be responsive and accessible
- File-based storage is not safe for concurrent users; consider database migration for multi-user support

## Dependencies
- streamlit
- pydantic (if used for data validation)
- Standard Python libraries (json, os, uuid, etc.)

## Tool Usage Patterns
- Streamlit for all user interactions
- Utility modules for data and export logic
- Modular codebase for maintainability
- Use of UUIDs for robust customer ID generation
- Plan for future migration to SQLite, PostgreSQL, or cloud DB for concurrency 