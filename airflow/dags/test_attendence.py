from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
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
    'simple_curl_dag',
    default_args=default_args,
    description='A simple DAG to trigger multiple curl commands sequentially',
    schedule_interval='0 1 * * *',  # Run daily at 1 AM
    catchup=False  # Don't run for past dates
)

# Function to run a curl command
def run_curl_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed with return code {result.returncode}: {result.stderr}")
    return result.stdout

# Define the Python tasks
curl_task_1 = PythonOperator(
    task_id='run_curl_1',
    python_callable=run_curl_command,
    op_args=['curl --location --request POST \'http://0.0.0.0:4448/api/v1/acquire/insert\' --header \'X-Custom-Passcode: ZG5OalFBPT0hISYhIU1qQXlNdz09\''],
    dag=dag,
)

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

# Define the task sequence
curl_task_1 >> curl_task_2_user >> curl_task_2_leave >> curl_task_2_leave_txn

