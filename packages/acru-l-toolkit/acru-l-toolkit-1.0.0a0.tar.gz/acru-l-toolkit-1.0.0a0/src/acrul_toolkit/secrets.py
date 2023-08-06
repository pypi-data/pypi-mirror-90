import json

import boto3


class Secrets:

    _secretsmanager = None

    @property
    def secretsmanager(self):
        if self._secretsmanager is None:
            self._secretsmanager = boto3.client("secretsmanager")
        return self._secretsmanager

    def get_secret(self, secret_id: str, key: str = None):
        secret_string = self.secretsmanager.get_secret_value(
            SecretId=secret_id
        )["SecretString"]
        if key:
            return json.loads(secret_string)[key]
        return secret_string


secrets = Secrets()
