"""
### Snowflake Tutorial DAG

This DAG demonstrates how to use the SQLExecuteQueryOperator, 
SnowflakeSqlApiOperator and SQLColumnCheckOperator to interact with Snowflake.
"""

from airflow.decorators import dag
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.common.sql.operators.sql import SQLColumnCheckOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeSqlApiOperator
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from airflow.models.baseoperator import chain
from pendulum import datetime, duration
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
import os

_SNOWFLAKE_CONN_ID = "snowflake_conn"
_SNOWFLAKE_DB = "ABACUSTEST"
_SNOWFLAKE_SCHEMA = "ABACUSSCHEMA"
_SNOWFLAKE_TABLE = "person_iceberg"


@dag(
    dag_display_name="Snowflake Tutorial DAG ❄️",
    start_date=datetime(2024, 9, 1),
    schedule=None,
    catchup=False,
    default_args={"owner": "airflow", "retries": 0,"snowflake_conn_id": _SNOWFLAKE_CONN_ID, "retry_delay": duration(seconds=5)},
    doc_md=__doc__,
    tags=["tutorial"],
    template_searchpath=[
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../include/sql")
    ],  # path to the SQL templates
)
def my_snowflake_dag():

    # you can execute SQL queries directly using the SQLExecuteQueryOperator
    select_data = SQLExecuteQueryOperator(
        task_id="select_data",
        conn_id=_SNOWFLAKE_CONN_ID,
        database="ABACUSTEST",
        sql=f"""
            select * from ABACUSTEST.ABACUSSCHEMA.person_iceberg    
        """,
    )

    snowflake_op_template_file = SnowflakeOperator(
    task_id="snowflake_op_template_file",
    sql="multiple_statements_query.sql",
    )
    # you can also execute multiple SQL statements using the SnowflakeSqlApiOperator
    # make sure to set the statement_count parameter to the number of statements in the SQL file
    # and that your connection details are in their proper capitalized form!
    multiple_statements = SnowflakeSqlApiOperator(
        task_id="multiple_statements",
        snowflake_conn_id=_SNOWFLAKE_CONN_ID,
        sql="multiple_statements_query.sql",
        database=_SNOWFLAKE_DB,
        schema=_SNOWFLAKE_SCHEMA,
        params={
            "db_name": _SNOWFLAKE_DB,
            "schema_name": _SNOWFLAKE_SCHEMA,
            "table_name": _SNOWFLAKE_TABLE,
        },
        statement_count=2,  # needs to match the number of statements in the SQL file
        autocommit=True,
    ) 

    chain(
        select_data,
        snowflake_op_template_file,
        multiple_statements,

    )


my_snowflake_dag()