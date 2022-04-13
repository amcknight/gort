import openai

respond_preamble = 'This is an ongoing intelligent and fun conversation happening on a twitch stream chat. This is the transcript:'

preamble = 'My name is \'robogort\' and I am an honest and highly intelligent Super Mario World Romhack question answering bot. I will answer questions as truthfully as possible in a single sentence. If you ask me a question I am unsure about, is nonsense, or has no clear answer, I will respond with "PASS".'
question_prefix = 'Q:'
answer_prefix = 'A:'
qa_pair_delimiter = '###'
qa_pairs = [
    ['robogort, which romhack is harder, Akogare or Grang Poo World 2?', 'Most people think GPW2 is harder.'],
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

max_tokens = 40

def preprompt():
    prom = preamble + '\n\n'
    for (question, answer) in qa_pairs:
        prom += question_prefix + ' ' + question + '\n' + answer_prefix + ' ' + answer + '\n'
        prom += qa_pair_delimiter + '\n'
    if last_ask[0] is not None:
        last_q, last_a = last_ask
        prom += question_prefix + ' ' + last_q + '\n' + answer_prefix + ' ' + last_a + '\n'
        prom += qa_pair_delimiter + '\n'

    prom += question_prefix
    return prom

def extract_answer_line(raw_answer):
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

def min_stop_index(text, ignore_prefix):
    indexes = list(filter(lambda i : i > -1, (text[ignore_prefix:].find(i) for i in '.!?')))
    if len(indexes) > 0:
        return min(indexes) + ignore_prefix
    return

def stop_index(text):
    late_index = min_stop_index(text, 12)
    if late_index:
        return late_index

    index = min_stop_index(text, 0)
    if index:
        return index

    return -1

def extract_response_line(raw_response):
    return first_nonblank_line(raw_response)
    
def first_nonblank_line(raw_response):
    lines = map(lambda l: strip_prefixes(l.strip()), raw_response.split('\n'))
    return next(filter(lambda l: len(l) > 0, lines), None)

def strip_prefixes(line):
    if line[0] in '/!':
        return line[1:]
    return line

def ask(question):
    global last_ask
    raw_answer = complete(preprompt() + question + '\n' + answer_prefix)
    answer = extract_answer_line(raw_answer)
    if not answer:
        return
    last_ask = [question, answer]
    if answer.lower().startswith('pass') or len(answer) < 2:
        return
    
    return answer

def respond(history, speaker, attempts=2):
    prompt = '\n'.join(history + [f'{speaker}:'])[-500:]
    attempts_left = attempts
    while attempts_left > 0:
        raw_response = complete(prompt)
        line = extract_response_line(raw_response)
        if line:
            return line
        attempts_left -= 1
    return

def complete(prompt, stops = None):
    # The main prompt completer
    global max_tokens
    response = openai.Completion.create(
        engine="curie",
        prompt=prompt,
        max_tokens=max_tokens,
        stop=stops
    )
    text = response.choices[0].text
    return text

def complete_haiku(topic):
    prompt = f'{haiku_prompt}\n{topic.strip()}\nHAIKU:'
    return complete(prompt, stops = ["TOPIC"])

def complete_best3(topic):
    prompt = f"""
List the 3 best ice cream:
1. Double chocolate
2. Raspberry Rainbow ice cream
3. Magical Hyper-enhanced Vanilla

List the best 3 {topic}:
1."""
    return complete(prompt, stops = ['4.']).strip()

haiku_prompt = f"""
Below is a list of creative and properly formed haikus in the 5 by 7 by 5 format.

TOPIC:
Ponds
HAIKU:
An old silent pond
A frog jumps into the pond—
Splash! Silence again.

TOPIC:
Relaxing
HAIKU:
Picking up pebbles
Or seashells strewn on soft sand
Pure relaxation.

TOPIC:
Dreams
HAIKU:
A plane flies over,
you dream of being on it.
Ideas flourish.

TOPIC:
Babies
HAIKU:
You're so cute, but why
Should I write a haiku for you?
You can't even read.

TOPIC:
Stinky Cheese
HAIKU:
I love you so much,
But your love of cheese is wrong.
The smell makes me gag.

TOPIC:
kaizo
HAIKU:
This game is too hard
I can't pass the first level
Someone help me please

TOPIC:"""