import os
import boto3
import json

class Env():
    def __init__(self):
        secrets_name = os.environ['SECRETS_NAME']
        secrets_region = os.environ['SECRETS_REGION']
        if secrets_name and secrets_region:
            self.secret = self.load_secrets(secrets_name, secrets_region)

        self.tmi_token = self.get('TMI_TOKEN')
        self.bot_nick = self.get('BOT_NICK')
        self.client_secret = self.get('CLIENT_SECRET')
        self.channel = self.get('CHANNEL')
        self.openai_api_key = self.get('OPENAI_API_KEY')

    def get(self, name):
        val = os.environ[name] or self.secret and self.secret[name]
        if val:
            return val
        else:
            exit(f"Couldn't find {name} in Environment Variables or Amazon Secrets Manager")
    
    def load_secrets(self, name, region):
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region)
        response = client.get_secret_value(SecretId=name)
        secret_str = response['SecretString']
        return json.loads(secret_str)
