from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import subprocess

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'run_raw_dag',
    default_args=default_args,
    description='Run raw ETL task once a day',
    schedule_interval='0 1 * * *',  # Run daily at 1 AM
    catchup=False
)

# Function to run a curl command
def run_curl_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed with return code {result.returncode}: {result.stderr}")
    return result.stdout
# Task to trigger the raw ETL
run_raw_task = PythonOperator(
    task_id='run_curl_raw',
    python_callable=run_curl_command,
    op_args=['curl --location --request POST \'http://0.0.0.0:4448/api/v1/acquire/insert\' --header \'X-Custom-Passcode: ZG5OalFBPT0hISYhIU1qQXlNdz09\''],
    dag=dag,
)

run_raw_task

