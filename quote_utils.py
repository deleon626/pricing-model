import json
import os
from datetime import datetime
import uuid

QUOTES_FILE = "data/quotes.json"

def generate_quote_id():
    """Generates a unique quote ID."""
    return f"QTE-{uuid.uuid4().hex[:8].upper()}"

def load_quotes():
    """Loads quotes from the JSON file."""
    if not os.path.exists(os.path.dirname(QUOTES_FILE)):
        os.makedirs(os.path.dirname(QUOTES_FILE))
    if not os.path.exists(QUOTES_FILE):
        return []
    try:
        with open(QUOTES_FILE, "r") as f:
            # Handle empty file case
            content = f.read()
            if not content:
                return []
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [] # Return empty list if file not found or invalid JSON

def save_quotes(quotes):
    """Saves the quotes list to the JSON file."""
    if not os.path.exists(os.path.dirname(QUOTES_FILE)):
        os.makedirs(os.path.dirname(QUOTES_FILE))
    with open(QUOTES_FILE, "w") as f:
        json.dump(quotes, f, indent=2, default=str) # Use default=str for datetime

def add_quote(customer_id, project_name, questionnaire, production_vars, low_quote, high_quote, recommended_quote, line_items):
    """Adds a new quote to the list and saves it."""
    quotes = load_quotes()
    
    new_quote = {
        "quote_id": generate_quote_id(),
        "customer_id": customer_id,
        "project_name": project_name or "Untitled Project",
        "questionnaire_snapshot": questionnaire,
        "production_vars_snapshot": production_vars,
        "low_quote": low_quote,
        "high_quote": high_quote,
        "recommended_quote": recommended_quote,
        "line_items_snapshot": line_items, # Consider if storing full line items is necessary or if they can be regenerated
        "status": "Draft", # Initial status
        "creation_date": datetime.now(),
        "last_updated_date": datetime.now()
    }
    quotes.append(new_quote)
    save_quotes(quotes)
    return new_quote # Return the newly created quote

def get_quotes_by_customer(customer_id):
    """Retrieves all quotes associated with a specific customer ID."""
    quotes = load_quotes()
    return [quote for quote in quotes if quote.get("customer_id") == customer_id]

def get_quote_by_id(quote_id):
    """Retrieves a single quote by its ID."""
    quotes = load_quotes()
    for quote in quotes:
        if quote.get("quote_id") == quote_id:
            return quote
    return None

def update_quote(quote_id, updates):
    """Updates an existing quote and saves the changes."""
    quotes = load_quotes()
    quote_found = False
    for i, quote in enumerate(quotes):
        if quote.get("quote_id") == quote_id:
            # Preserve creation date, update last_updated_date
            updates["last_updated_date"] = datetime.now()
            creation_date = quote.get("creation_date") # Keep original creation date
            
            quotes[i].update(updates)
            
            # Ensure creation date wasn't overwritten if it existed
            if creation_date and "creation_date" not in updates:
                 quotes[i]["creation_date"] = creation_date
                 
            quote_found = True
            break
            
    if quote_found:
        save_quotes(quotes)
        return True
    return False

def update_quote_status(quote_id, new_status):
    """Updates the status of a specific quote."""
    return update_quote(quote_id, {"status": new_status})

# Example Usage (Optional - for testing)
if __name__ == '__main__':
    # Make sure the data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
        
    # Example: Add a dummy quote
    # dummy_q = {"q1": "A"}
    # dummy_p = {"p1": "B"}
    # dummy_lines = [{"item": "Service A", "cost": 100}]
    # added = add_quote("CUST-123", "Test Project", dummy_q, dummy_p, 90, 110, 100, dummy_lines)
    # print(f"Added Quote: {added}")

    # Example: Get quotes for a customer
    # cust_quotes = get_quotes_by_customer("CUST-123")
    # print(f"Quotes for CUST-123: {cust_quotes}")
    
    # Example: Update status
    # if cust_quotes:
    #     update_status_result = update_quote_status(cust_quotes[0]['quote_id'], "Quoted")
    #     print(f"Update status result: {update_status_result}")
    #     updated_quote = get_quote_by_id(cust_quotes[0]['quote_id'])
    #     print(f"Updated Quote: {updated_quote}")
    
    print("Quote utils loaded.")
    # Initialize with an empty list if file doesn't exist or is empty
    if not os.path.exists(QUOTES_FILE) or os.path.getsize(QUOTES_FILE) == 0:
        save_quotes([])
        print(f"Initialized empty {QUOTES_FILE}") 