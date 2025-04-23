import json
import os
from datetime import datetime

# File to store customer data
CUSTOMERS_FILE = "customers.json"

def load_customers():
    """Load customer data from JSON file"""
    if os.path.exists(CUSTOMERS_FILE):
        try:
            with open(CUSTOMERS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"customers": []}
    else:
        # Create a new file with empty customers array
        save_customers({"customers": []})
        return {"customers": []}

def save_customers(data):
    """Save customer data to JSON file"""
    with open(CUSTOMERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_customer(customer):
    """Save a single customer to the list"""
    data = load_customers()
    
    # Check if customer already exists (by ID)
    for i, existing in enumerate(data["customers"]):
        if existing["customer_id"] == customer["customer_id"]:
            # Update existing customer
            data["customers"][i] = customer
            save_customers(data)
            return True
    
    # Add new customer
    data["customers"].append(customer)
    save_customers(data)
    return True

def get_customer(customer_id):
    """Get a specific customer by ID"""
    data = load_customers()
    for customer in data["customers"]:
        if customer["customer_id"] == customer_id:
            return customer
    return None

def add_project_to_customer(customer_id, project_info):
    """Add a project to a customer's history"""
    customer = get_customer(customer_id)
    if not customer:
        return False
    
    if "project_history" not in customer:
        customer["project_history"] = []
    
    # Add timestamp if not provided
    if "date" not in project_info:
        project_info["date"] = datetime.now().strftime("%Y-%m-%d")
    
    customer["project_history"].append(project_info)
    return save_customer(customer)

def search_customers(query):
    """Search customers by name, email, or company"""
    data = load_customers()
    results = []
    
    query = query.lower()
    for customer in data["customers"]:
        if (query in customer.get("name", "").lower() or
            query in customer.get("email", "").lower() or
            query in customer.get("company", "").lower()):
            results.append(customer)
    
    return results

def delete_customer(customer_id):
    """Delete a customer by ID from the customers list."""
    data = load_customers()
    original_count = len(data["customers"])
    data["customers"] = [c for c in data["customers"] if c["customer_id"] != customer_id]
    save_customers(data)
    return len(data["customers"]) < original_count 