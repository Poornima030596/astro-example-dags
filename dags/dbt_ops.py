from __future__ import annotations

from datetime import datetime

from airflow.models import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.dbt.cloud.operators.dbt import (
    DbtCloudGetJobRunArtifactOperator,
    DbtCloudListJobsOperator,
    DbtCloudRunJobOperator,
)

with DAG(
    dag_display_name="DBT_OPS",
    dag_id="DBT_OPS",
    default_args={"dbt_cloud_conn_id": "dbt"},
    start_date=datetime(2021, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    trigger_job_run1 = DbtCloudRunJobOperator(
        task_id="trigger_job_run1",
        job_id=737128,
        check_interval=10,
        timeout=300,
        )