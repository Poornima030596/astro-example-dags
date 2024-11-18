from airflow import DAG
from airflow.operators.python import PythonOperator 
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from datetime import timedelta

region_name='eu-west-1' 
glue_job_name='dev.dpf_dag_003_nhe_incremental_raw.account'  #Refer to Image below

from datetime import datetime

def _start():
    print('Hi')

def _end():
    print('Job end')

with DAG('dag_glue_script', catchup=False) as dag:

    start = PythonOperator(
        task_id='start',
        python_callable=_start 
    )
    start_glue_job = GlueJobOperator(
        job_name=glue_job_name,
        task_id='run',
        aws_conn_id='aws_default',
        create_job_kwargs={"GlueVersion": "1.0", "NumberOfWorkers": 10, "WorkerType": "G.1X"},
        stop_job_run_on_kill=True,
        verbose=True,
        wait_for_completion=True,
        deferrable=True,
        job_poll_interval=15
    )

    end = PythonOperator(
        task_id='end',
        python_callable=_end
    )

start >> start_glue_job >> end