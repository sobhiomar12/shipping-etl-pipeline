from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def hello():
    print("✅ Airflow is working!")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

with DAG(
    'hello_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    
    task = PythonOperator(
        task_id='hello_task',
        python_callable=hello,
    )