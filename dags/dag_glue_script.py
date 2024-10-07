from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator

region_name='eu-west-1' 
glue_job_name='sit_qtc_glue_oracle_r12_snowflake_full_ORACLE_R12_AR_TRX_QTC_SNF_LOAD'  #Refer to Image below

from datetime import datetime

def _start():
    print('Hi')

def _end():
    print('Job end')

with DAG('dag_glue_script', start_date=datetime(2024,1,1,),schedule_interval='@daily', catchup=False) as dag:

    start = PythonOperator(
        task_id='start',
        python_callable=_start 
    )

    start_glue_job = GlueJobOperator(
        task_id = "RunGlueJob",
        job_name = glue_job_name,
        job_desc = "qtc_glue_oracle_r12_snowflake_full",
        region_name = region_name,
        iam_role_name = "business-analytics-pipelines-glue-service-role-sit",
        script_location=f"s3://com-elsevier-business-analytics-nonprod/sit/work/resources/r12_extract_glue_script.py",
        #script_args={'--abc':'1','--pqr':'2'},
        create_job_kwargs={"GlueVersion": "4.0", "NumberOfWorkers": 10, "WorkerType": "G.1X"},
        aws_conn_id='aws_default',
        stop_job_run_on_kill=True,
        verbose=True,
        dag = dag
        )

    end = PythonOperator(
        task_id='end',
        python_callable=_end
    )

start >> start_glue_job >> end