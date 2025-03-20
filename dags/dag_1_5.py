from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow import DAG

import sys
sys.path.append('/opt/airflow/assign2')

from main12 import main12
from main3 import main3
from main4 import main4

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 14),
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    default_args=default_args,
    description='Dag for module 1, 2, 3, 4, 5',
    dag_id='dag_hourly_scraper',
    start_date=datetime(2025, 2, 16),
    schedule_interval='@hourly',
    catchup=False
) as dag:
    task12 = PythonOperator(
        task_id="main12",
        python_callable=main12
    )
    task3 = PythonOperator(
        task_id="main3",
        python_callable=main3
    )
    task4 = PythonOperator(
        task_id="main4",
        python_callable=main4
    )

    task12 >> task3 >> task4