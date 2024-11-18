from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import boto3
import pandas as pd
from sqlalchemy import create_engine

# Set your S3 bucket details and Airflow DB connection string
S3_BUCKET = 'aws-astro-edps-test'
S3_PREFIX = 'nhe'
DB_CONNECTION = 'postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/postgres'

def export_metadata_to_s3():
    # Connect to the metadata database
    engine = create_engine(DB_CONNECTION)

    # Define tables to export (modify as needed)
    tables = ['dag', 'task_instance', 'job', 'log', 'xcom']

    s3_client = boto3.client('s3')
    for table in tables:
        # Export each table to a DataFrame
        df = pd.read_sql_table(table, con=engine)
        # Convert DataFrame to CSV
        csv_data = df.to_csv(index=False)

        # Define S3 path for each table
        s3_key = f"{S3_PREFIX}/{table}/{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # Upload CSV to S3
        s3_client.put_object(Body=csv_data, Bucket=S3_BUCKET, Key=s3_key)

# DAG definition
with DAG(
    'export_airflow_metadata_to_s3',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    export_task = PythonOperator(
        task_id='export_metadata_to_s3',
        python_callable=export_metadata_to_s3
    )
