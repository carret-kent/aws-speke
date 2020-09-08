import abc

class CacheDriver(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def exists(self, content_id: str, key_id: str) -> bool:
        pass

    @abc.abstractmethod
    def get(self, content_id: str, key_id: str):
        pass

    @abc.abstractmethod
    def store(self, content_id: str, key_id: str, content) -> str:
        pass

    @abc.abstractmethod
    def derived_url(self, content_id: str, key_id: str) -> str:
        pass
