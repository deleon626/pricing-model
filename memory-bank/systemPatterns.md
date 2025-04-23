# System Patterns

## System Architecture
- Modular Python application with clear separation between UI, business logic, and data handling.
- Uses Streamlit for the user interface.
- Core logic and utilities are separated into distinct modules (e.g., pricing_logic.py, customer_utils.py, export_utils.py).

## Key Technical Decisions
- Chose Streamlit for rapid UI development and ease of use.
- Data is managed in JSON files for simplicity and portability.
- Pricing logic is encapsulated for maintainability and extensibility.
- Loaded quote state is tracked in Streamlit session state for correct UI behavior (e.g., save vs. update logic).
- Customer IDs are generated using UUIDs for uniqueness and robustness.

## Design Patterns
- Separation of concerns: UI, logic, and data are decoupled.
- Utility modules for reusable functions.
- Template-driven exports for flexibility.
- Error handling for file operations using try/except blocks with user-friendly feedback.

## Component Relationships
- UI components interact with business logic modules to fetch, process, and display data.
- Data flows from JSON files through logic modules to the UI and export functions.
- Session state is used to manage loaded quote and active tab for improved user experience.

## Critical Implementation Paths
- Data import/export pipeline
- Pricing calculation workflow
- UI event handling and feedback
- Quote management workflow (save, update, load, clear, and navigation)
- Error handling and user guidance 