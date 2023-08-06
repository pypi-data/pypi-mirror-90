import base64
import boto3
import re

from botocore.exceptions import ClientError

from SecretManagerEnvInjector.exceptions import InvalidInputException

class SecretExtractor():

    def __init__(self):
        self.session = boto3.session.Session()
        self.secret_name = None

    def _validate_input(self, arn: str):
        result = re.search(r'(arn:aws:secretsmanager:.+:\d+:secret:)(.+)', arn)
        if result is None:
            raise InvalidInputException(msg='Invalid ARN')
            return
        self.secret_name = result.group(2)

    def extract(self, secret_arn: str, region_name: str):
        secret = None
        self._validate_input(secret_arn)
        client = self.session.client(service_name = 'secretsmanager', region_name = region_name)
        try:
            response = client.get_secret_value(SecretId = secret_arn)
            if 'SecretString' in response:
                secret = response['SecretString']
            else:
                secret = base64.b64decode(response['SecretBinary'])
            return secret
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ExpiredToken':
                # token used for calling has expired
                raise e
            elif e.response['Error']['Code'] == 'AccessDeniedException':
                # unauthorized user access
                raise e

    def get_secret_name(self):
        if self.secret_name:
            return self.secret_name
        return 'extracted_secret'