from cache_driver_abc import CacheDriver

class CacheMock(CacheDriver):

    def exists(self, content_id: str, key_id: str) -> bool:
        return False

    def get(self, content_id: str, key_id: str):
        return b'\x07o\xa8X\x04\x18\xe5\x04V<\xd2\xf7\xe0\xa1\xa9}'

    def store(self, content_id: str, key_id: str, content) -> str:
        return self.derived_url(content_id, key_id)

    def derived_url(self, content_id: str, key_id: str) -> str:
        return 'https://exsample.com/{content_id}/{key_id}'.format(content_id=content_id, key_id=key_id)
