import openai

respond_preamble = 'This is an ongoing intelligent and fun conversation happening on a twitch stream chat. The streamer is mangort and is playing Super Mario World romhacks. robogort is mangort\'s polite and honest comedian robot. This is the transcript:'

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

last_ask = [None, None]

max_tokens = 30

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

def extract_response_line(raw_response):
    response_line = raw_response.split('\n')[0]
    if len(response_line) < 150:
        return response_line
    
    trunc_index = max(response_line.rfind(i) for i in '.!?')
    return response_line[:trunc_index]


def ask(question):
    global last_ask
    raw_answer = complete(preprompt() + question + '\n' + answer_prefix)
    answer = extract_answer_line(raw_answer)
    if not answer:
        return
    last_ask = [question, answer]
    if answer.startswith('PASS') or answer.startswith('pass') or answer.startswith('Pass') or len(answer) < 2:
        return
    
    return answer

def respond(history, author):
    truncated_history = '\n'.join(history + [f'robogort: @{author}'])[-400:]
    prompt = respond_preamble + '\n\n' + truncated_history
    raw_response = complete(prompt)
    return extract_response_line(raw_response)

def complete(prompt):
    global max_tokens
    response = openai.Completion.create(engine="curie", prompt=prompt, max_tokens=max_tokens)
    print(response)
    exit
    return response.choices[0].text