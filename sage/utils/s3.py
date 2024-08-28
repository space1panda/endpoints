# Stream data directly to S3

import boto3
import requests
from io import BytesIO
import logging
from omegaconf import OmegaConf


logger = logging.getLogger()

def stream_to_s3(config):
    """
    The script expects the existance of URLs 
    publicly available for downloading
    """
    dataset_name = config.dataset
    chunk_size = config.chunk_size
    s3_bucket = config.bucket_name
    urls = config.urls

    s3 = boto3.client('s3')

    for url in urls:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Upload the streamed data directly to S3
        with BytesIO() as data_stream:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # Filter out keep-alive new chunks
                    data_stream.write(chunk)
            data_stream.seek(0)  # Go to the start of the BytesIO object
            s3.upload_fileobj(data_stream, s3_bucket, 'file.csv')

        logger.info("File uploaded successfully!")