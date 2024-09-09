import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import os
import base64
from datetime import datetime
from database import DataSourceConfiguration
from services.LeaveTxnService import LeaveTxnService
leave_txn_service = LeaveTxnService(DataSourceConfiguration.mysql_datasource)

def get_sample():
    json_file = leave_txn_service.find_data()
    df = pd.json_normalize(json_file)
    return df

def get_data(start_date=None,end_date=None):
    json_file = leave_txn_service.find_data(start_date,end_date)
    df = pd.json_normalize(json_file)
    return df

def save_plot_to_file(plt, filename):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Current timestamp
    filename = f"{filename}_{timestamp}.png" 
    static_dir = "static"  # Make sure this directory exists or create it if necessary
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)  # Create the static directory if it does not exist
    file_path = os.path.join(static_dir, filename)
    plt.savefig(file_path, format='png')
    plt.close()  # Close the plot after saving to prevent memory leaks
    return filename 

# Helper function to save plot as base64 string
def save_plot_as_base64(plt):
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return img_base64

# Function 1: Bar Chart for Leave Requests by Department
def department_analysis(df):
    plt.figure(figsize=(10, 8))
    department_counts = df['department_description'].value_counts()
    department_counts.plot(kind='bar', color='skyblue')
    plt.title('Leave Requests by Department')
    plt.xlabel('Department')
    plt.ylabel('Number of Requests')
    return save_plot_as_base64(plt)
    #return save_plot_to_file(plt,'dept')

# Function 2: Pie Chart for Supervisor vs Non-Supervisor Leave Requests
def supervisor_analysis_part2(df):
    plt.figure(figsize=(10, 8))
    
    # Count the number of supervisor vs non-supervisor entries
    supervisor_counts = df['is_supervisor'].value_counts()
    
    # Generate dynamic labels based on the unique values in the is_supervisor column
    labels = supervisor_counts.index.map(lambda x: 'Supervisor' if x else 'Non-Supervisor')
    
    # Create the pie chart
    plt.pie(supervisor_counts, labels=labels, autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue'])
    plt.title('Supervisor vs Non-Supervisor Leave Requests')
    return save_plot_as_base64(plt) #return save_plot_to_file(plt,'sup')

def supervisor_analysis(df):
    plt.figure(figsize=(8, 8))
    df['leave_status'].value_counts().plot.pie(autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    plt.title('Leave Status Distribution')
    
    return save_plot_as_base64(plt) 


# Function 3: Bar Chart for Leave Requests by Designation
def designation_analysis(df):
    plt.figure(figsize=(10, 8))
    designation_counts = df['designation_name'].value_counts()
    designation_counts.plot(kind='bar', color='orange')
    plt.title('Leave Requests by Designation')
    plt.xlabel('Designation')
    plt.ylabel('Number of Requests')
    return save_plot_as_base64(plt) #return save_plot_to_file(plt,'des')

# Function 4: Histogram for Leave Days Distribution
def leave_days_analysis_(df):
    plt.figure(figsize=(10, 8))
    plt.hist(df['leave_days'], bins=5, color='green')
    plt.title('Leave Days Distribution')
    plt.xlabel('Leave Days')
    plt.ylabel('Frequency')
    return save_plot_as_base64(plt) #return save_plot_to_file(plt,'leave')

def leave_days_analysis(df):
    # Define the mapping from leave_type_id to leave type names
    leave_type_mapping = {
        8: 'Annual',
        13: 'Maternity',
        14: 'Paternity',
        11: 'Leave Without Pay',
        12: 'Bereavement',
        9: 'Sick',
        10: 'Well-being',
        15: 'Menstruation',
        7: 'Discretionary'
    }
    
    # Map leave_type_id to leave type names
    df['leave_type'] = df['leave_type_id'].map(leave_type_mapping)
    
    # Count occurrences of each leave type
    leave_counts = df['leave_type'].value_counts()
    
    # Define the order for leave types, if needed (optional)
    ordered_leave_types = [
        'Annual', 'Maternity', 'Paternity', 'Leave Without Pay',
        'Bereavement', 'Sick', 'Well-being', 'Menstruation', 'Discretionary'
    ]
    
    # Sort counts based on the defined order
    counts = [leave_counts.get(leave_type, 0) for leave_type in ordered_leave_types]
    
    plt.figure(figsize=(10, 8))
    plt.barh(ordered_leave_types, counts, color='skyblue')
    plt.title('Leave Type Distribution')
    plt.xlabel('Number of Requests')
    plt.ylabel('Leave Type')
    plt.gca().invert_yaxis()  # Invert y-axis for better readability
    plt.grid(True)
    
    # Save the plot as a base64 string or show it (depends on your requirements)
    return save_plot_as_base64(plt)