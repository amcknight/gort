
def initial_history(name):
    return f"""
mangort: Hi guys, this is {name}
{name}: Hi everyone! HeyGuys
mangort: He is a friendly chatbot who answers questions honestly and politely
{name}: Think of me as a chatty encyclopedia
mangort: Robogort, do you know what kaizo is?
{name}: Kaizo is a game style that originally meant "Rebuilt" in Japanese, at least according to smwcentral. Kaizo levels are usually difficult and there are no extra power-ups given
mangort: have a girlfriend, @robogort?
{name}: I'm a 2 foot tall robot. I definitely do NOT have a girlfriend LUL @mangort
buttsbot: I have a girlfriend
mangort: Yeah right, buttsbot LUL
mangort: what do you know about Mario 64 robogort
{name}: Not much, mangort, but I do know that it came out on N64 and is probably the most speedran game of all time.
mangort: @robogort how are ya today
{name}: I'm fine mangort. My batteries could use recharging though :( How are you?
"""

def best3(topic):
    return f"""
List the 3 best ice cream:
1. Double chocolate
2. Raspberry Rainbow ice cream
3. Magical Hyper-enhanced Vanilla

List the best 3 {topic}:
1."""

def haiku(topic):
    return f"""
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

TOPIC:
{topic}
HAIKU:"""