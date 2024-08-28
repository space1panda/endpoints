import logging
import boto3
from botocore.config import Config


logger = logging.getLogger(__name__)


config = Config(
    connect_timeout=5,
    read_timeout=10,
    retries={'max_attempts': 1}
    )


def checkAWSaccess():
    """
    Simple check of whether the AWS resources can be accessed from current environment
    """

    try:
        s3 = boto3.client('s3', config=config)
        response = s3.list_buckets()
        logger.info(f'AWS account access success: {response}')
    except Exception as e:
        logger.critical(e)
