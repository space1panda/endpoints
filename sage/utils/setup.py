import logging
import boto3
import time
import datetime
from botocore.exceptions import ClientError
from .connectivity import config as connection_cfg
import json


logger = logging.getLogger(__name__)


def _stringtime(obj):
    obj = list(obj)
    if isinstance(obj[1], datetime.datetime):
        obj[1] = obj[1].isoformat()
    return tuple(obj)


def setSageIAMrole(config):
    """
    Creates IAM Role with necessary permissions for accessing Sagemaker services
    """

    role_name = config.role_name
    region = config.region
    trust_policy_path = config.trust_policy_path
    policies = config.role_policies

    iam_client = boto3.client(
        'iam', region_name=region, config=connection_cfg)
    try:
        response = iam_client.get_role(RoleName=role_name)
        arn = response['Role']['Arn']
        logger.info(f'The role already exists: {arn}')
        response = dict(map(_stringtime, response['Role'].items()))
        return response
    except ClientError as cl_er:
        error = cl_er.response['Error']['Code']
        if error == 'NoSuchEntity':
            logger.info(f'Creating Sagemaker role {role_name}')

            with open(trust_policy_path, 'r') as tp:
                policy = json.dumps(json.load(tp))
            
            response = iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=policy,
                Description='Role for SageMaker to access AWS resources'
            )
            for pol in policies:
                iam_client.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=pol
                )

            logger.info(f"Attached policies to role: {policies}")
            logger.info(f'Role {role_name} successfully created')
        else:
            logger.critical(cl_er)


def setSageDomain(config, role_arn):
    """
    Creates a Domain for using cloud IDE and other services provided by Sagemaker
    """

    domain_name = config.domain_name
    vpcid = config.vpcid
    subnets = list(config.subnets)
    sagemaker_client = boto3.client(
        'sagemaker', region_name=config.region,
        config=connection_cfg)
    
    try:
        domains = sagemaker_client.list_domains().get('Domains')
        if domains is not None:
            domains = {d['DomainName']: d for d in domains}
    except Exception as err:
        logger.critical(f"Cannot list domains: {err}")

    if domain_name in domains:
        logger.info(f'Domain {domain_name} already exists')
        response = sagemaker_client.describe_domain(
            DomainId=domains[domain_name]['DomainId'])
    else:
        logger.info(f'Creating Sagemaker domain {domain_name}')
        response = sagemaker_client.create_domain(
            DomainName=domain_name,
            AuthMode='IAM',
            DefaultUserSettings={
                'ExecutionRole': role_arn,
            },
            VpcId=vpcid,
            SubnetIds=subnets,
        )

        while True:
            response = sagemaker_client.describe_domain(
                DomainId=response.get('DomainArn').split('/')[-1])
            if response.get('Status') == 'InService':
                break
            else:
                time.sleep(20)
                continue

        logger.info(f'Sagemaker Domain {domain_name} successfully created')
    response = dict(map(_stringtime, response.items()))
    return response

