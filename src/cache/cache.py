import os

from cache_driver_mock import CacheMock
from cache_driver_s3 import CacheS3

class Cache:
    def __init__(self):
        """
        If APP_ENV is local. use Mock Class
        """
        self.driver = CacheMock() if os.environ['APP_ENV'] == 'local' else CacheS3()

    def exists(self, content_id: str, key_id: str) -> bool:
        return self.driver.exists(content_id, key_id)

    def get(self, content_id: str, key_id: str) -> str:
        return self.driver.get(content_id, key_id)

    def store(self, content_id: str, key_id: str, content) -> str:
        return self.driver.store(content_id, key_id, content)

    def derived_url(self, content_id: str, key_id: str) -> str:
        return  self.driver.derived_url(content_id, key_id)
