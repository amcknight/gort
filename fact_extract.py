suspicious_pointer_words = ['he', 'she', 'they', 'this', 'said', 'says']

section_delimiter = '-----'
facts_prefix = ') '
transcript_header_prefix = 'PARTIAL TRANSCRIPT #'
facts_header_prefix = 'EXTRACTED FACTS #'
transcript1 = '''
robogort: Hi everyone, how can I help you?
mangort: Hi robogort!
robogort: You looking for some of that cheer @mangort
mangort: I am robogort! :D Do you like cheese?
robogort: Yes, cheese is nice @mangort
mangort: @robogort Do you have a favourite kind of cheese?
robogort: Cheese fan @mangort
mangort: @robogort What kind is your fav?
robogort: Yes @mangort, cheese is greasy
mangort: My favourite type of cheese is gouda
mangort: Do you have one?
robogort: @mangort 's mama makes gouda cheese!
'''
facts1 = [
    "1) @mangort 's favourite cheese is gouda.",
    "2) @robogort likes cheese.",
    "3) @robogort thinks @mangort 's mother makes gouda."
]
transcript2 = '''
robogort: Hi everyone, how can I help you?
joe: I'm going to play Hark 2 before Invictus
ted532: @robogort What do you think of SMW romhacks?
robogort: Not much, I was doing the run for whatever reason @ted532
ted532: @robogort What were you running?
robogort: Them (SMB Land) @ted532
joe: SMB land. Cool! When were you born, robogort?
robogort: 83 @joe
joe: 1983?
robogort: Yeah today is my 29th birthday @joe
ted532: What year do you think it is @robogort ...
robogort: A year like the one before that or a year before that
'''
facts2 = [
    "1) @robogort thinks he is 29 years old.",
    "2) @joe is playing Hark 2 before Invictus.",
    "3) @robogort thinks he was doing SMB Land runs."
]
transcript3 = '''
Skipped64: mario POGGERS
bmac15120: mario on the mind????
hi_im_kai_: jump :)
yourclassnerd: OH NO not down there
Brahman1000: bowsaaa widepeepoHappy
sofiawithnof: is mario like a friend of yours or something
fearfall_tv: Depends what you’re going for but there is no right and wrong sofia
Der_Religionslehrer: Only total degens play Mario. It's old and boring.
slaff23: do some god bridging PogU
yourclassnerd: restart
Skipped64: @der_religionslehrer judging by your name u are old and boring too tho drozConcern
hi_im_kai_: the perfect amount for you
'''
facts3 = [
    '1) @Der_Religionslehrer thinks only degenerates play Mario.'
]
def fact_extraction_prompt(transcript):
    return '\n'.join(
        [
            section_delimiter,
            transcript_header_prefix + '1',
            section_delimiter,
            transcript1,
            section_delimiter,
            facts_header_prefix + '1',
            section_delimiter,
            '\n'.join(facts1),
            section_delimiter,
            transcript_header_prefix + '2',
            section_delimiter,
            transcript2,
            section_delimiter,
            facts_header_prefix + '2',
            section_delimiter,
            '\n'.join(facts2),
            section_delimiter,
            transcript_header_prefix + '3',
            section_delimiter,
            transcript3,
            section_delimiter,
            facts_header_prefix + '3',
            section_delimiter,
            '\n'.join(facts3),
            section_delimiter,
            transcript_header_prefix + '4',
            section_delimiter,
            transcript,
            section_delimiter,
            facts_header_prefix + '4',
            section_delimiter,
            '1)'
        ]
    )
