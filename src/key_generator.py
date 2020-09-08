import string
import secrets

from cache import Cache
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class KeyGenerator:
    """
    This class is responsible for symmetric key generation.
    """
    def __init__(self, cache: Cache):
        self.backend = default_backend()
        self.content_id_secret_length = 64
        self.derived_key_iterations = 5000
        self.derived_key_size = 16
        self.cache = cache

    def derived_key(self, secret: str, kid: str) -> str:
        """
        Generate a key using a key derivation function (default)
        """
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=self.derived_key_size, salt=secret.encode('utf-8'), iterations=self.derived_key_iterations, backend=self.backend)
        return kdf.derive(kid.encode('utf-8'))

    def generate_secret(self) -> str:
        """
        Generate a string of random text used in generating a key for a content ID/key ID
        """
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~'
        return ''.join(secrets.choice(chars) for _ in range(self.content_id_secret_length))

    def hls_aes_128(self, content_id: str, key_id: str) -> str:
        """
        Return Deriver Key and Path

        If cache exists return to cache
        Else key generate and store cache
        """
        if (self.cache.exists(content_id, key_id)):
            print('CACHE HIT')
            return self.cache.get(content_id, key_id), self.cache.derived_url(content_id, key_id)

        derived_key = self.derived_key(self.generate_secret(), key_id)
        derived_url = self.cache.store(content_id, key_id, derived_key)

        return derived_key, derived_url
