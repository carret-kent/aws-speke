import os
import boto3
from cache_driver_abc import CacheDriver

class CacheS3(CacheDriver):
    KEY_STORE_BUCKET = os.environ['KEY_STORE_BUCKET']
    KEY_STORE_BUCKET_PREFIX = os.environ['KEY_STORE_BUCKET_PREFIX']
    DERIVED_DOMAIN_URL = os.environ['DERIVED_DOMAIN_URL']

    def __init__(self):
        self.s3_client = boto3.client('s3')

    def exists(self, content_id: str, key_id: str) -> bool:
        try:
            content = self.s3_client.head_object(Bucket=self.KEY_STORE_BUCKET, Key=self.store_object_path(content_id, key_id))
            return content.get('ResponseMetadata', None) is not None
        except Exception as exception:
            return False

    def get(self, content_id: str, key_id: str):
        response = self.s3_client.get_object(Bucket=self.KEY_STORE_BUCKET, Key=self.store_object_path(content_id, key_id))
        return response['Body'].read()

    def store(self, content_id: str, key_id: str, content) -> str:
        self.s3_client.put_object(Bucket=self.KEY_STORE_BUCKET, Key=self.store_object_path(content_id, key_id), Body=content)
        return self.derived_url(content_id, key_id)

    def derived_url(self, content_id: str, key_id: str) -> str:
        return '{domain}/{path}'.format(domain=self.DERIVED_DOMAIN_URL, path=self.store_object_path(content_id, key_id))

    def store_object_path(self, content_id: str, key_id: str):
        if self.KEY_STORE_BUCKET_PREFIX == '':
            return '/'.join([content_id, key_id])

        return '/'.join([self.KEY_STORE_BUCKET_PREFIX, content_id, key_id])

