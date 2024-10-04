import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import os
import base64
from datetime import datetime
from database import DataSourceConfiguration
from services.LeaveTxnService import LeaveTxnService
from services.UserService import UserService
leave_txn_service = LeaveTxnService(DataSourceConfiguration.mysql_datasource)
user_service = UserService(DataSourceConfiguration.mysql_datasource)


def user_details(username):
    json_file = user_service.find_user_data(username)
    return json_file


def get_sample():
    json_file = leave_txn_service.find_data()
    df = pd.json_normalize(json_file)
    return df

def get_data(start_date=None,end_date=None,filter_params=None):
    json_file = leave_txn_service.find_data(start_date,end_date,filter_params)
    df = pd.json_normalize(json_file)
    return df

def get_leave_data(emp_id=None):
    json_file = leave_txn_service.find_leave_balance(emp_id)
    return json_file

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
    plt.close()
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return img_base64


def visualize_leave_data(df):
    # Grouping data by leave type to sum up leave taken and available leave
    summary = df.groupby('leave_type').agg(
        total_available_leave=('available_leave', 'sum'),
        total_leave_taken=('leave_taken', 'sum'),
        total_users=('emp_id', lambda x: x.nunique())  # Count unique users
    ).reset_index()

    # Visualization: Bar Chart - Leave Taken and Available Leave by Leave Type
    plt.figure(figsize=(10, 5))

    # Bar for total leave taken
    plt.bar(summary['leave_type'], summary['total_leave_taken'], color='#1f77b4', label='Total Leave Taken')  # Distinct color

    # Bar for available leave
    plt.bar(summary['leave_type'], summary['total_available_leave'], 
            bottom=summary['total_leave_taken'], color='#ff7f0e', label='Total Available Leave')  # Distinct color

    # Display total users on top of each bar
    for i, row in summary.iterrows():
        plt.text(row.name, row.total_leave_taken + row.total_available_leave + 1, 
                 f'Users: {row.total_users}', ha='center', color='black')

    plt.title('Leave Taken and Available Leave by Leave Type')
    plt.xlabel('Leave Type')
    plt.ylabel('Leave (Days)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    return save_plot_as_base64(plt)

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

    # Calculate total leave days per department
    total_leave_days_per_department = department_designation_stats.groupby('department_description')['leave_days'].sum().reset_index()
    total_leave_days_per_department.rename(columns={'leave_days': 'total_leave_days'}, inplace=True)

    # Merge the total leave days into the original stats
    department_designation_stats = pd.merge(department_designation_stats, total_leave_days_per_department, on='department_description')

    # Calculate the percentage of leave days for each designation within each department
    department_designation_stats['leave_days_percentage'] = (department_designation_stats['leave_days'] / department_designation_stats['total_leave_days']) * 100

    # Handle cases with more than 5 unique departments or designations
    def get_top_n_and_others(group, n=5):
        top_n = group.nlargest(n, 'leave_days_percentage')
        others = group[~group.index.isin(top_n.index)]
        others = pd.DataFrame({'department_description': ['Other'], 'leave_days_percentage': [others['leave_days_percentage'].sum()]})
        return pd.concat([top_n, others])

    # Handle departments and designations separately
    department_stats = department_designation_stats.groupby('department_description').apply(lambda x: get_top_n_and_others(x, n=5)).reset_index(drop=True)
    designation_stats = department_designation_stats.groupby('designation_name').apply(lambda x: get_top_n_and_others(x, n=5)).reset_index(drop=True)

    # Pivot table for leave days percentage by department and designation
    pivot_table_percentage = department_stats.pivot_table(
        index='department_description',
        columns='designation_name',
        values='leave_days_percentage',
        fill_value=0
    )

    # Plot leave days percentage by department and designation
    plt.subplot(1, 1, 1)
    pivot_table_percentage.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='viridis', edgecolor='black')
    plt.title('Percentage of Leave Days by Department and Designation')
    plt.xlabel('Department')
    plt.ylabel('Leave Days (%)')
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
    
    # Convert leave days into percentage of total leave days for each month
    pivot_table_percentage = pivot_table.div(pivot_table['Total'], axis=0) * 100
    
    # Drop the 'Total' column as it's no longer needed for the percentage plot
    pivot_table_percentage = pivot_table_percentage.drop(columns=['Total'])
    
    # Sort months by total leave days
    sorted_months = pivot_table_percentage.index
    
    # Create a bar chart for leave requests by month and department (percentage)
    plt.figure(figsize=(14, 10))
    
    # Define colors
    colors = plt.cm.viridis(range(0, 256, int(256/len(pivot_table_percentage.columns))))
    
    # Plot bars for each department (as percentage)
    for i, department in enumerate(pivot_table_percentage.columns):
        plt.barh(pivot_table_percentage.index, pivot_table_percentage[department], color=colors[i], label=department, edgecolor='black', height=0.8)
    
    plt.title('Percentage of Total Leave Requests by Month and Department')
    plt.xlabel('Percentage of Requests')
    plt.ylabel('Month')
    plt.legend(title='Department')
    plt.gca().invert_yaxis()  # Invert y-axis for better readability
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save or return plot as needed
    return save_plot_as_base64(plt)


def leave_type_pie_chart(df):
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
    
    # Filter out 'Leave Without Pay' (leave_type_id = 11)
    df_filtered = df[df['leave_type_id'] != 11]

    # Calculate the total leave days for each leave type
    leave_type_summary = df_filtered.groupby('leave_type')['leave_days'].sum().reset_index()

    # Plot a pie chart for the leave type distribution
    plt.figure(figsize=(8, 8))
    plt.pie(
        leave_type_summary['leave_days'], 
        labels=leave_type_summary['leave_type'], 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=plt.cm.Paired.colors, 
        wedgeprops={'edgecolor': 'black'}
    )
    
    plt.title('Leave Type Distribution (Excluding Leave Without Pay)')
    plt.axis('equal')  # Equal aspect ratio ensures the pie is circular.

    # Save or return the pie chart as needed
    return save_plot_as_base64(plt)

def leave_type_bar_chart(df):
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
    
    # Filter out 'Leave Without Pay' (leave_type_id = 11)
    df_filtered = df[df['leave_type_id'] != 11]

    # Calculate the total leave days for each leave type
    leave_type_summary = df_filtered.groupby('leave_type')['leave_days'].sum().reset_index()

    # Calculate the percentage of leave days for each type
    total_leave_days = leave_type_summary['leave_days'].sum()
    leave_type_summary['percentage'] = (leave_type_summary['leave_days'] / total_leave_days) * 100

    # Plot a bar chart for the leave type distribution by percentage
    plt.figure(figsize=(10, 6))
    plt.barh(leave_type_summary['leave_type'], leave_type_summary['percentage'], color='skyblue', edgecolor='black')

    plt.title('Leave Type Percentage Distribution (Excluding Leave Without Pay)')
    plt.xlabel('Percentage of Total Leave Days')
    plt.ylabel('Leave Type')

    # Display the percentage on each bar
    for index, value in enumerate(leave_type_summary['percentage']):
        plt.text(value + 0.5, index, f'{value:.1f}%', va='center')

    plt.tight_layout()

    # Save or return the bar chart as needed
    return save_plot_as_base64(plt)
