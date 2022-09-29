import openai


class Completer(openai.Completion):
    def __delitem__(self, k):
        pass  # TODO: Look into what this is for

    def __init__(self, engine, max_tokens, **kwargs):
        super().__init__(**kwargs)
        self.max_tokens = max_tokens
        self.engine = engine

    def complete(self, prompt, stops=None):
        # The main prompt completer
        response = openai.Completion.create(
            engine=self.engine,
            max_tokens=self.max_tokens,
            prompt=prompt,
            stop=stops
        )
        text = response.choices[0].text
        return text
