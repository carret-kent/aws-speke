import sys
sys.path.append('./cache')
sys.path.append('./lib')

import traceback
from cache import Cache
from key_generator import KeyGenerator
from speke_response_builder import SpekeResponseBuilder
from speke_request_validator import SpekeRequestValidator


def lambda_handler(event, context):
    try:
        print('REQUEST_EVENT {}\n'.format(str(event)))
        """
        init
        """
        cache = Cache()

        """
        validation
        """
        validator = SpekeRequestValidator(event['body'], event['isBase64Encoded'])
        if validator.fail():
            raise SyntaxError('Please check your request')

        body = validator.get_body()
        content_id = validator.get_content_id()
        key_id = validator.get_key_id()

        print('BODY {}\n'.format(body))
        print('CONTENT_ID {}\n'.format(content_id))
        print('KID {}\n'.format(key_id))

        """
        Generate KeyBytes
        """
        Generator = KeyGenerator(cache)
        key_bytes, derived_url = Generator.hls_aes_128(content_id, key_id)
        print('KEY_BYTES {}\n'.format(key_bytes))
        print('URL {}\n'.format(derived_url))

        """
        Generate response body
        """
        response = SpekeResponseBuilder(body, content_id, key_id, key_bytes, derived_url).get_response()
        return response
    except Exception as exception:
        t, v, tb = sys.exc_info()
        print('EXCEPTION {}\n'.format(str(exception)))
        print(traceback.format_exception(t, v, tb))
        print(exception.__traceback__)
        return {'isBase64Encoded': False, 'statusCode': 500, 'headers': {'Content-Type': 'text/plain'}, 'body': str(exception)}
