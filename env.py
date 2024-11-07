import os
import boto3
import json

class _Env():
    "Creates a Global wrapped OS / Amazon Secret Manager initialization object. Instance at the bottom."
    
    def __init__(self):
        self.secret = self.load_secrets()
        self.set_env()

    def load_secrets(self):
        try:
            session = boto3.session.Session()
            client = session.client(service_name='secretsmanager', region_name=os.environ['SECRETS_REGION'])
            response = client.get_secret_value(SecretId=os.environ['SECRETS_NAME'])
            secret_str = response['SecretString']
            return json.loads(secret_str)
        except KeyError:
            return False # Silently fails to load from Amazon Secrets Manager

    def set_env(self):
        self.bot_nick = self.get('BOT_NICK')
        upnick = self.bot_nick.upper()
        self.tmi_token = self.get('TMI_TOKEN', fallback=f"{upnick}_TMI_TOKEN")
        self.client_secret = self.get('CLIENT_SECRET', fallback=f"{upnick}_CLIENT_SECRET")
        self.channel = self.get('CHANNEL')
        self.completer = self.get('COMPLETER')

        if self.completer == 'claude':
            self.anthropic_api_key = self.get('ANTHROPIC_API_KEY')
        if self.completer == 'gpt4o-mini':
            self.openai_api_key = self.get('OPENAI_API_KEY')
        elif self.completer == 'gpt3.5':
            self.openai_api_key = self.get('OPENAI_API_KEY')
        elif self.completer == 'gpt3':
            self.openai_api_key = self.get('OPENAI_API_KEY')
            self.engine = self.get('ENGINE')
        else:
            raise ValueError(f'Invalid completer "{self.completer}"')

    def get(self, key, fallback=None):
        try:
            return os.environ[key]
        except KeyError as e:
            if not self.secret:
                raise e
            
            try:
                return self.secret[key]
            except KeyError as e:
                if fallback:
                    return self.secret[fallback]
                raise e

env = _Env()
