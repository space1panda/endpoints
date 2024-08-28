import boto3
import sagemaker
from sagemaker.processing import ScriptProcessor,\
    ProcessingInput, ProcessingOutput
from sagemaker.session import Session


def main():
    config = {
        'region_name': 'east-us-1'
    }

    session = Session(
        boto_session=boto3.Session(region_name='east-us-1'))
    role = sagemaker.get_execution_role(session)
    region = session.boto_region_name


# # Initialize a SageMaker client
# sagemaker_client = boto3.client('sagemaker')

# # Define the processing job parameters
# processing_job_name = 'my-processing-job'
# role_arn = 'arn:aws:iam::your-account-id:role/your-sagemaker-role'
# bucket_name = 'your-bucket-name'
# input_data_key = 'path/to/input-data.csv'
# output_data_key = 'path/to/output-data.csv'
# script_path = 'path/to/my_processing_script.py'

# # Create a Processing Job
# response = sagemaker_client.create_processing_job(
#     ProcessingJobName=processing_job_name,
#     RoleArn=role_arn,
#     AppSpecification={
#         'ImageUri': 'your-docker-image-uri',  # Use a pre-built SageMaker image or your custom image
#         'ContainerEntrypoint': ['python3', '/opt/ml/processing/input/code/my_processing_script.py'],
#     },
#     ProcessingInputs=[
#         {
#             'InputName': 'input-data',
#             'S3Input': {
#                 'S3Uri': f's3://{bucket_name}/{input_data_key}',
#                 'LocalPath': '/opt/ml/processing/input/data',
#                 'S3DataType': 'S3Prefix',
#                 'S3InputMode': 'File',
#             }
#         }
#     ],
#     ProcessingOutputs=[
#         {
#             'OutputName': 'output-data',
#             'S3Output': {
#                 'S3Uri': f's3://{bucket_name}/{output_data_key}',
#                 'LocalPath': '/opt/ml/processing/output/data',
#                 'S3OutputMode': 'File',
#             }
#         }
#     ],
#     ProcessingResources={
#         'ClusterConfig': {
#             'InstanceType': 'ml.m5.xlarge',
#             'InstanceCount': 1,
#             'VolumeSizeInGB': 30,
#         }
#     },
#     StoppingCondition={
#         'MaxRuntimeInSeconds': 3600
#     }
# )

# print(f"Processing job created: {response['ProcessingJobArn']}")


if __name__ == '__main__':
    main()