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
def supervisor_analysis(df):
    plt.figure(figsize=(16, 10))

    # Print column names and first few rows for debugging
    print("Columns in DataFrame:", df.columns)
    print("First few rows of DataFrame:\n", df.head())

    # Check if 'designation_name' column exists
    if 'designation_name' not in df.columns:
        raise ValueError("Column 'designation_name' does not exist in the DataFrame")

    # Create a new column for supervisors
    df['is_supervisor'] = df['designation_name'].apply(
        lambda x: 1 if x in ['Team Lead', 'VP of Engineering'] else 0
    )

    # Aggregate leave statistics by department and designation
    department_designation_stats = df.groupby(['department_description', 'designation_name'])['leave_days'].sum().reset_index()
    
    # Aggregate and handle cases with more than 5 unique departments or designations
    def get_top_n_and_others(group, n=5):
        top_n = group.nlargest(n, 'leave_days')
        others = group[~group.index.isin(top_n.index)]
        others = pd.DataFrame({'department_description': ['Other'], 'leave_days': [others['leave_days'].sum()]})
        return pd.concat([top_n, others])

    # Handle departments and designations separately
    department_stats = department_designation_stats.groupby('department_description').apply(lambda x: get_top_n_and_others(x, n=5)).reset_index(drop=True)
    designation_stats = department_designation_stats.groupby('designation_name').apply(lambda x: get_top_n_and_others(x, n=5)).reset_index(drop=True)
    
    # Pivot table for total leave days by department and designation
    pivot_table_total = department_stats.pivot_table(
        index='department_description',
        columns='designation_name',
        values='leave_days',
        fill_value=0
    )

    # Plot total leave days by department and designation
    plt.subplot(1, 1, 1)
    pivot_table_total.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='viridis', edgecolor='black')
    plt.title('Total Leave Days by Department and Designation')
    plt.xlabel('Department')
    plt.ylabel('Total Leave Days')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Designation')
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()

    # Save or return plot as needed
    return save_plot_as_base64(plt)



# Function 3: Bar Chart for Leave Requests by Designation
def designation_analysis(df):
    plt.figure(figsize=(10, 8))
    designation_counts = df['designation_name'].value_counts()
    
    # Get the top 5 designations
    top_designations = designation_counts.head(5)
    
    # Combine other designations into 'Others'
    other_designations_count = designation_counts.iloc[5:].sum()
    
    # Create a new Series for 'Others' and concatenate with top_designations
    other_designations = pd.Series({'Others': other_designations_count})
    top_designations = pd.concat([top_designations, other_designations])
    
    # Create a pie chart
    plt.pie(top_designations, labels=top_designations.index, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    plt.title('Leave Requests by Designation (Top 5 + Others)')
    
    return save_plot_as_base64(plt)  # return save_plot_to_file(plt,'des')

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
    
    # Extract month and year from the start_date
    df['month'] = pd.to_datetime(df['start_date']).dt.to_period('M').astype('str')
    
    # Convert month period to month name and year
    df['month_name'] = pd.to_datetime(df['month']).dt.strftime('%B %Y')
    
    # Aggregate leave days by month_name and department
    monthly_department_summary = df.groupby(['month_name', 'department_description'])['leave_days'].sum().reset_index()
    
    # Pivot table to get department distribution per month
    pivot_table = monthly_department_summary.pivot(index='month_name', columns='department_description', values='leave_days').fillna(0)
    
    # Calculate the total leave days for each month
    pivot_table['Total'] = pivot_table.sum(axis=1)
    
    # Sort months by total leave days
    sorted_months = pivot_table.sort_values(by='Total', ascending=False).index
    
    # Create a bar chart for leave requests by month and department
    plt.figure(figsize=(14, 10))
    
    # Define colors
    colors = plt.cm.viridis(range(0, 256, int(256/len(pivot_table.columns))))
    
    # Plot bars for each department
    for i, department in enumerate(pivot_table.columns[:-1]):  # Exclude 'Total'
        plt.barh(pivot_table.index, pivot_table[department], color=colors[i], label=department, edgecolor='black', height=0.8)
    
    plt.title('Total Leave Requests by Month and Department')
    plt.xlabel('Number of Requests')
    plt.ylabel('Month')
    plt.legend(title='Department')
    plt.gca().invert_yaxis()  # Invert y-axis for better readability
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save or return plot as needed
    return save_plot_as_base64(plt)
