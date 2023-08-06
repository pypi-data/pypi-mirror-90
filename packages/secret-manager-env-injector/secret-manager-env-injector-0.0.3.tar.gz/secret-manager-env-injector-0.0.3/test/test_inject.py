import unittest
import os

from SecretManagerEnvInjector import inject

class InjectTest(unittest.TestCase):

    @inject('arn:aws:secretsmanager:us-east-1:xxxxxxxxxxxxxx:secret:bogus-dj3g0R')
    def test_inject(self):
        self.assertEquals(os.getenv('bogus-dj3g0R'), 'test2')