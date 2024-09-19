from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.hooks.mysql_hook import MySqlHook
import subprocess

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'status_check_dag',
    default_args=default_args,
    description='A DAG that checks status and triggers appropriate ETL tasks',
    schedule_interval='*/5 * * * *',  # Run every 5 minutes
    catchup=False  # Don't run for past dates
)

# Function to check the latest status in MySQL
def check_status():
    mysql_hook = MySqlHook(mysql_conn_id='attendence')  # Set your connection ID
    query = """
    SELECT status_type FROM Attendence_System.Status
    WHERE started_at >= CURDATE() AND status = 1
    ORDER BY started_at DESC
    LIMIT 1;
    """
    result = mysql_hook.get_first(query)
    if result:
        status_type = result[0]
        if status_type == 'Raw':
            return 'run_curl_2_user'
        elif status_type == 'User':
            return 'run_curl_2_leave'
        elif status_type == 'Leave':
            return 'run_curl_2_leave_txn'
        elif status_type == 'LeaveTxn':
    	    return 'run_curl_2_designation'
        return 'no_task_to_run'

# Define the branch task that decides which task to run
branch_task = BranchPythonOperator(
    task_id='check_status',
    python_callable=check_status,
    dag=dag,
)

# Function to run a curl command
def run_curl_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed with return code {result.returncode}: {result.stderr}")
    return result.stdout

# Define the Python tasks
curl_task_2_user = PythonOperator(
    task_id='run_curl_2_user',
    python_callable=run_curl_command,
    op_args=['curl --location \'http://0.0.0.0:4448/api/v1/etl/load\' --header \'X-Custom-Passcode: ZG5OalFBPT0hISYhIU1qQXlNdz09\' --form \'etl_name="user"\''],
    dag=dag,
)

curl_task_2_leave = PythonOperator(
    task_id='run_curl_2_leave',
    python_callable=run_curl_command,
    op_args=['curl --location \'http://0.0.0.0:4448/api/v1/etl/load\' --header \'X-Custom-Passcode: ZG5OalFBPT0hISYhIU1qQXlNdz09\' --form \'etl_name="leave"\''],
    dag=dag,
)

curl_task_2_leave_txn = PythonOperator(
    task_id='run_curl_2_leave_txn',
    python_callable=run_curl_command,
    op_args=['curl --location \'http://0.0.0.0:4448/api/v1/etl/load\' --header \'X-Custom-Passcode: ZG5OalFBPT0hISYhIU1qQXlNdz09\' --form \'etl_name="leave_txn"\''],
    dag=dag,
)

curl_task_2_designation = PythonOperator(
    task_id='run_curl_2_designation',
    python_callable=run_curl_command,
    op_args=['curl --location \'http://0.0.0.0:4448/api/v1/etl/load\' --header \'X-Custom-Passcode: ZG5OalFBPT0hISYhIU1qQXlNdz09\' --form \'etl_name="designation"\''],
    dag=dag,
)

# Dummy task if no status to run
def no_op():
    return 'No task to run'

no_task_to_run = PythonOperator(
    task_id='no_task_to_run',
    python_callable=no_op,
    dag=dag,
)

# Define the task sequence
branch_task >> [curl_task_2_user, curl_task_2_leave, curl_task_2_leave_txn,curl_task_2_designation, no_task_to_run]
