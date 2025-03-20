# Get connection on Airflow UI from SMTP servers and Postgres

import os
from airflow import DAG
from datetime import datetime, timedelta
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 16),
    'email': ['nikshay.p.jain@gmail.com'],
    'default_email_on_failure': True,
    'default_email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dag_email_on_new_data',
    default_args=default_args,
    description='Send email when new data is added to the database',
    schedule_interval=None,
    catchup=False
)

def check_new_rows(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    # Get the current row count
    cursor.execute("SELECT COUNT(*) FROM headlines")
    current_count = cursor.fetchone()[0]

    # Get the previous count from XCom
    ti = kwargs['ti']
    previous_count = ti.xcom_pull(task_ids='check_new_rows', key='previous_count')

    if previous_count is None:
        previous_count = 0

    new_rows = current_count - previous_count

    # Store the current count for the next run
    ti.xcom_push(key='previous_count', value=current_count)

    return new_rows

def delete_status_file():
    os.remove('/opt/airflow/dags/run/status')

file_sensor = FileSensor(
    task_id='wait_for_status_file',
    filepath='/opt/airflow/dags/run/status',
    poke_interval=60,
    timeout=3600,
    dag=dag
)

check_rows = PythonOperator(
    task_id='check_new_rows',
    python_callable=check_new_rows,
    provide_context=True,
    dag=dag
)

send_email = EmailOperator(
    task_id='send_email',
    to='nikshay.p.jain@gmail.com',
    subject='New Data Added to Database',
    html_content='{{ task_instance.xcom_pull(task_ids="check_new_rows") }} new rows have been added to the database.',
    dag=dag
)

delete_file = PythonOperator(
    task_id='delete_status_file',
    python_callable=delete_status_file,
    dag=dag
)

file_sensor >> check_rows >> send_email >> delete_file