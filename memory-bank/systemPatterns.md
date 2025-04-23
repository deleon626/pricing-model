# System Patterns

## System Architecture
- Modular Python application with clear separation between UI, business logic, and data handling.
- Uses Streamlit for the user interface.
- Core logic and utilities are separated into distinct modules (e.g., pricing_logic.py, customer_utils.py, export_utils.py).

## Key Technical Decisions
- Chose Streamlit for rapid UI development and ease of use.
- Data is managed in JSON files for simplicity and portability.
- Pricing logic is encapsulated for maintainability and extensibility.

## Design Patterns
- Separation of concerns: UI, logic, and data are decoupled.
- Utility modules for reusable functions.
- Template-driven exports for flexibility.

## Component Relationships
- UI components interact with business logic modules to fetch, process, and display data.
- Data flows from JSON files through logic modules to the UI and export functions.

## Critical Implementation Paths
- Data import/export pipeline
- Pricing calculation workflow
- UI event handling and feedback 