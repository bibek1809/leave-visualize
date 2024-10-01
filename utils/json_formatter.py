import json

def format_leave_data(raw_json):
    """
    Formats the given raw JSON data into a structured dictionary by employee ID.

    Args:
        raw_json (str or list): Raw JSON string or list containing leave data.

    Returns:
        str: Formatted JSON string grouped by employee ID.
    """
    # Check if the input is a string and needs conversion
    if isinstance(raw_json, str):
        # Replace single quotes with double quotes for valid JSON
        json_string = raw_json.replace("'", '"')
        # Load the JSON string into a Python list
        data = json.loads(json_string)
    elif isinstance(raw_json, list):
        # If already a list, use it directly
        data = raw_json
    else:
        raise ValueError("Input must be a JSON string or a list.")

    # Initialize the result dictionary
    formatted_data = {}

    # Populate the formatted_data dictionary
    for entry in data:
        emp_id = entry['emp_id']
        leave_info = {
            "available_leave": entry["available_leave"],
            "leave_taken": entry["leave_taken"],
            "leave_type": entry["leave_type"],
            "total_leave": entry["total_leave"]
        }

        # Initialize the employee entry if it doesn't exist
        if emp_id not in formatted_data:
            formatted_data[emp_id] = []

        # Append the leave information to the employee's list
        formatted_data[emp_id].append(leave_info)

    # Return the formatted data as a JSON string
    return json.dumps(formatted_data, indent=4)