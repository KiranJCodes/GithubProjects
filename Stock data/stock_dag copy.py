from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import sys
import os

'''
This is  just a copy of my DAG. 
the main file is stored in my airflow DAGs folder
'''


# Add your project path so Airflow can find your scripts
sys.path.insert(0, '/home/daydreamer/Github uploads/GithubProjects/Stock data')

def run_stock_script():
    """Function that runs your Main.py script"""
    import Main  # Import your script
    
    # If your Main.py has a main function, call it
    if hasattr(Main, 'main'):
        Main.main()
    else:
        print("Main block not found")
        

# Default arguments for the DAG
default_args = {
    'owner': 'daydreamer',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),  # Start from Jan 1, 2025
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'stock_price_pipeline',
    default_args=default_args,
    description='Fetches stock prices daily at 8 AM',
    schedule_interval='0 8 * * 1-5',  # At 8:00 AM every weekday
    catchup=False,  # Don't run for past dates
    tags=['stocks', 'daily'],
)

# Define the task
run_stock_task = PythonOperator(
    task_id='fetch_and_store_stock_prices',
    python_callable=run_stock_script,
    dag=dag,
)

# Single task DAG - just this task
run_stock_task
