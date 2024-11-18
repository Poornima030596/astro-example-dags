from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

region_name='eu-west-1' 
glue_job_name='dpf_dag_004_nhe_full_raw_nhe_s3_extractor_contact_dev'  #Refer to Image below

from datetime import datetime

def _start():
    print('Hi')

def _end():
    print('Job end')

with DAG('dag_glue_script4', catchup=False) as dag:

    start = PythonOperator(
        task_id='start',
        python_callable=_start 
    )
    start_glue_job = GlueJobOperator(
        task_id = "RunGlueJob",
        job_name = glue_job_name,
        job_desc = "dpf_dag_004_nhe_full_raw_nhe_s3_extractor_contact_dev",
        region_name = region_name,
        iam_role_name = "business-analytics-pipelines-glue-service-role-dev",
        script_location=f"s3://com-elsevier-business-analytics-pipelines-nhe-dev/dev/fullload/scripts/code/nhe_business_analytics_full_load/glue-scripts/nhe_full_load_glue_job_script.py",
        #script_args={'--abc':'1','--pqr':'2'},
        create_job_kwargs={"GlueVersion": "2.0", "NumberOfWorkers": 10, "WorkerType": "G.1X"},
        aws_conn_id='aws_default',
        stop_job_run_on_kill=True,
        verbose=True,
        dag = dag,
        wait_for_completion=True,
        job_poll_interval=15
        )

    end = PythonOperator(
        task_id='end',
        python_callable=_end
    )

start >> start_glue_job >> end