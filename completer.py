from openai import OpenAI
import inspect
from env import env

class Completer():
    def __init__(self, max_tokens):
        self.max_tokens = max_tokens

    def complete(self, prompt, stops=None):
        # The main prompt completer
        if env.completer == 'gpt3.5':
            return self.gpt35_turbo(prompt)
        elif env.completer == 'gpt3':
            return self.gpt3_base(prompt, stops=stops)
        
    
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
            self.client = OpenAI(api_key=env.openai_api_key, max_tokens=self.max_tokens)
        
        system_prompt = """
            Just complete the next few lines of response from the prompt given. Nothing extra.
            Try not to write for other people. Only robogort.
            Never mention being an assistant. You aren't! Be weird. Insults are ok.
            Write very tersly, like 2-15 words almost always.
            Don't be scared to use emotes (preferably Twitch emotes but normal emojis are ok too).
            Be genuinely random. Don't use proper sentence structure or spelling. Choose text a random chatter might choose.
            But try to respond within the context of the chat, riffing on it, rather than completely ignoring it.
            """
        system_prompt = inspect.cleandoc(system_prompt)
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
    