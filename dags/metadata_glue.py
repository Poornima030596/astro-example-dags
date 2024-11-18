from airflow.providers.amazon.aws.operators.s3_transfer import s3TransferOperator 

metadata_file='metadata.json'
transfer=s3TransferOperator (
    task_id='upload_metadata',
    bucket_key=f's3://aws-astro-edps-test/nhe',
    bucket='aws-astro-edps-test',
    upload_file_path=metadata_file
)