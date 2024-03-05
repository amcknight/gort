import completer
from text import best3, haiku


class Oracle(completer.Completer):

    preamble = 'My name is \'robogort\' and I am an honest and highly intelligent Super Mario World Romhack question answering bot. I will answer questions as truthfully as possible in a single sentence. If you ask me a question I am unsure about, is nonsense, or has no clear answer, I will respond with "PASS".'
    respond_preamble = 'This is an ongoing intelligent and fun conversation happening on a twitch stream chat. This is the transcript:'
    question_prefix = 'Q:'
    answer_prefix = 'A:'
    qa_pair_delimiter = '###'
    qa_pairs = [
        ['robogort, which romhack is harder, Akogare or Grand Poo World 2?', 'Most people think GPW2 is harder.'],
        ['which games were you talking about, robogort?','Akogare and Grand Poo World 2.'],
        ['Who made Rob Father?','DanOfMostTrades created Robfather World.'],
        ['How does a telescope work?','Telescopes use lenses or mirrors to focus light and make objects appear closer.'],
        ['when was dram made??','PangaeaPanga released Super Dram World on May 25th, 2015.'],
        ['Who made Storks?','Morsel made Storks and Apes and Crocodiles'],
        ['WHo is Dram?','dram55 is an American speedrunner known as the first person to complete Kaizo Mario World deathless.']
    ]
    beliefs = []
    # beliefs = [
    #     'Grand Poo World 2 is harder than Akogare.',
    #     '@robogort is a robot.',
    #     '@robogort is 2 feet tall, has a bronze finish, and alightning fast internet connection.',
    #     '@mangort is playing Hyperion which was made by AmperSam.',
    #     '@robogort just started dating a Smart Toaster named X78-3000.',
    #     'Being direct and honest is the best way to communicate.',
    #     'When someone asks a question, it is rude to not answer.',
    #     '@robogort has big eyes and a small mouth.',
    #     'X78-3000 is the most beautiful robot @robogort has ever met.',
    #     '@robogort is a polite, honest, question answering, comedian robot.'
    # ]

    last_ask = [None, None]

    def __init__(self, max_tokens, **kwargs):
        super().__init__(max_tokens, **kwargs)

    def preprompt(self):
        prom = self.preamble + '\n\n'
        for (question, answer) in self.qa_pairs:
            prom += self.question_prefix + ' ' + question + '\n' + self.answer_prefix + ' ' + answer + '\n'
            prom += self.qa_pair_delimiter + '\n'
        if self.last_ask[0] is not None:
            last_q, last_a = self.last_ask
            prom += self.question_prefix + ' ' + last_q + '\n' + self.answer_prefix + ' ' + last_a + '\n'
            prom += self.qa_pair_delimiter + '\n'

        prom += self.question_prefix
        return prom

    def extract_answer_line(self, raw_answer):
        trimmed_raw_answer = raw_answer.strip()
        infinity = 10000
        line_ends = ['.', '!', '?', '\n']
        line_end_replacements = ['.', '!', '?', '.']
        end_indexes = [(trimmed_raw_answer.index(d) if d in trimmed_raw_answer else infinity) for d in line_ends]

        min_i = min(end_indexes)
        if min_i == infinity:
            print('No end')
            return
        if min_i == 0:
            print('Immediate termination')
            return

        first_d = line_end_replacements[end_indexes.index(min_i)]

        return trimmed_raw_answer[0:min_i] + first_d

    def min_stop_index(self, text, ignore_prefix):
        indexes = list(filter(lambda i : i > -1, (text[ignore_prefix:].find(i) for i in '.!?')))
        if len(indexes) > 0:
            return min(indexes) + ignore_prefix
        return

    def stop_index(self, text):
        late_index = self.min_stop_index(text, 12)
        if late_index:
            return late_index

        index = self.min_stop_index(text, 0)
        if index:
            return index

        return -1

    def extract_response_line(self, raw_response):
        return self.first_nonblank_line(raw_response)

    def first_nonblank_line(self, raw_response):
        lines = map(lambda l: self.strip_prefixes(l.strip()), raw_response.split('\n'))
        return next(filter(lambda l: len(l) > 0, lines), None)

    def strip_prefixes(self, line):
        if line[0] in '/!':
            return line[1:]
        return line

    def ask(self, question):
        raw_answer = self.complete(self.preprompt() + question + '\n' + self.answer_prefix)
        answer = self.extract_answer_line(raw_answer)
        if not answer:
            return
        last_ask = [question, answer]
        if answer.lower().startswith('pass') or len(answer) < 2:
            return

        return answer

    def respond(self, history, speaker, attempts=2):
        prompt = '\n'.join(history + [f'{speaker}:'])[-500:]
        attempts_left = attempts
        while attempts_left > 0:
            raw_response = self.complete(prompt)
            line = self.extract_response_line(raw_response)
            if line:
                return line
            attempts_left -= 1
        return

    def complete_haiku(self, topic):
        return self.complete(haiku(topic.strip()), stops = ["TOPIC"]).strip()

    def complete_best3(self, topic):
        return self.complete(best3(topic.strip()), stops = ['4.']).strip()

