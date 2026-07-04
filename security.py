# security.py
# Check if the Input python dictionary keys all have values.
# Return (True, "") if all the keys in the dictionary do not have "" as the value
# else return (False, "Error: All fields must have a value")

def validate_inputs(inputs: dict) -> tuple[bool, str]:
    """
    Validates that all input fields are non-empty.
    
    Args:
        inputs: A dictionary containing the input keys.
        
    Returns:
        A tuple of (is_valid, error_message).
    """
    # The expected keys are client_name, client_desc, customer_domain, and project_overview.
    required_keys = ['client_name', 'client_desc', 'customer_domain', 'project_overview']
    
    for key in required_keys:
        if key not in inputs:
            return (False, f"Error: All fields must have a value. Missing '{key}'.")
        val = inputs[key]
        if not val or not isinstance(val, str) or val.strip() == "":
            return (False, "Error: All fields must have a value")
            
    return (True, "")
