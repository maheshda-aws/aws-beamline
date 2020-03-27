import json
import boto3
from botocore.exceptions import ClientError

# Assign the ID of an existing cluster to the following variable
job_flow_id = 'j-22C1QYTU1ILQK'

# Define a job flow step. Assign appropriate values as desired.
job_flow_step_01 = {
    'Name': 'SQLRunner',
    'ActionOnFailure': 'CONTINUE',
    'HadoopJarStep': {
        'Jar': 'command-runner.jar',
        'Args': [
            'spark-submit',
            '--deploy-mode', 'cluster',
            's3://maheshda-file-bucket/pyspark/spark-etl.py',
            's3://glue-crawler-test-maheshda/sample/my-tbl/2017/06/01/',
            's3://glue-crawler-test-maheshda/sample/my-tbl/out3/2017/06/01/'
        ]
    }
}

# Add the step(s)
emr_client = boto3.client('emr')
try:
    response = emr_client.add_job_flow_steps(JobFlowId=job_flow_id,
                                             Steps=[job_flow_step_01])
    print(response)
except ClientError as e:
    print(e.response['Error']['Message'])
    exit(1)

# Output the IDs of the added steps
print('Step IDs:')
for stepId in response['StepIds']:
    print(stepId)
