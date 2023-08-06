import os
import logging

from SecretManagerEnvInjector.secret_extractor import SecretExtractor

logger = logging.getLogger()

def inject(secret_arn: str, region: str = 'us-east-1', custom_secret_name:str = None):
    def inner_wrap(func):
        def wrap(*args, **kwargs):
            try:
                extractor = SecretExtractor()
                secret = extractor.extract(secret_arn, region)
                if custom_secret_name is None:
                    secret_name = extractor.get_secret_name()
                else:
                    secret_name = custom_secret_name
                if secret:
                    os.environ[str(secret_name)] = secret
            except Exception as ex:
                logger.error('Exception: {}'.format(ex))
            return func(*args, **kwargs)
        return wrap
    return inner_wrap

if __name__ == '__main__':
    @inject('arn:aws:secretsmanager:us-xxxx-1:xxxxxxxxxxx:secret:bogus-dj3g0R', 'us-east-1', 'my-secret')
    def test():
        print("hello")
    test()