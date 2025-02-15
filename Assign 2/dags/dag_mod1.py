from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow import DAG

import sys
sys.path.append('/opt/airflow/assign2')

from main12 import main12
from main3 import main3

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 2, 14),
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    default_args=default_args,
    description='Dag for module 1, 2, 3',
    dag_id='dag_mod123',
    start_date=datetime(2025, 2, 14),
    schedule_interval='@daily'
) as dag:
    task12 = PythonOperator(
        task_id="main12",
        python_callable=main12
    )
    task3 = PythonOperator(
        task_id="main3",
        python_callable=main3
    )

    task12 >> task3