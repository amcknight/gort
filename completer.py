import logging
from openai import OpenAI
import anthropic
import inspect
from env import env

logging.basicConfig(filename='log.log', level=logging.INFO, format='%(levelname)-7s:%(asctime)s> %(message)s', datefmt='%b-%d %H:%M:%S')

class Completer():
    def __init__(self, max_tokens):
        self.max_tokens = max_tokens

    def complete(self, prompt, stops=None):
        # The main prompt completer
        if env.completer == 'gpt4o-mini':
            return self.gpt4o_mini(prompt)
        elif env.completer == 'gpt3.5':
            return self.gpt35_turbo(prompt)
        elif env.completer == 'gpt3':
            return self.gpt3_base(prompt, stops=stops)
        elif env.completer == 'claude':
            return self.claude(prompt)
        else:
            logging.error(f'No completer named "{env.completer}"')
        
    default_system_prompt = """
        Just complete the next few lines of response from the prompt given. Nothing extra.
        Try not to write for other people. Only robogort.
        Never mention being an assistant. You aren't! Be weird. Insults are ok.
        Write very tersly, like 2-15 words almost always.
        Don't be scared to use emotes (preferably Twitch emotes but normal emojis are ok too).
        Be genuinely random. Don't use proper sentence structure or spelling. Choose text a random chatter might choose.
        But try to respond within the context of the chat, riffing on it, rather than completely ignoring it.
        """
    
    def gpt3_base(self, prompt, stops=None):
        import openai
        response = openai.Completion.create(
            api_key=env.openai_api_key,
            engine=env.engine,
            max_tokens=self.max_tokens,
            prompt=prompt,
            stop=stops
        )
        text = response.choices[0].text
        return text

    def gpt35_turbo(self, prompt):
        if not hasattr(self, 'client'):
            self.client = OpenAI(api_key=env.openai_api_key)
        
        system_prompt = inspect.cleandoc(self.default_system_prompt)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
        )
        choices = response.choices
        choice = choices[0]
        message = choice.message
        text = message.content
        return text
    
    def gpt4o_mini(self, prompt):
        if not hasattr(self, 'client'):
            self.client = OpenAI(api_key=env.openai_api_key)
        
        system_prompt = inspect.cleandoc(self.default_system_prompt)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]
        )
        choices = response.choices
        choice = choices[0]
        message = choice.message
        text = message.content
        return text
    
    def claude(self, prompt):
        self.client = anthropic.Anthropic(api_key=env.anthropic_api_key)
        system_prompt = inspect.cleandoc(self.default_system_prompt)
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=self.max_tokens,
            temperature=0,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": prompt
                }]
            }]
        )
        contents = response.content
        content = contents[0]
        text = content.text
        return text
