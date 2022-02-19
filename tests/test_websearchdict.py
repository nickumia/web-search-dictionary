
import websearchdict
import websearchdict.web.constants as wwc


# Provide acceptable order of the number of definitions
# Varies depending on google search

def test_lookup():
    definitions = websearchdict.lookup('equal')
    # print(definitions.getDefinitions())
    assert definitions.getPronounciation() == '/ˈēkwəl/ | '
    assert 2 <= len(definitions.getDefinitions()) <= 6
    assert__pos(definitions.getDefinitions())


def test_example():
    # Get the definitions for 'special'
    entry = websearchdict.lookup('special')

    # Get the pronounciation for 'special'
    print(entry.getPronounciation())

    # Get the definitions
    for key, sense in entry.getDefinitions().items():
        print('Part of speech [%d]: %s' % (key, sense['pos']))
        print('Definition [%d]: %s' % (key, sense['definition']))


def test_lookup_a():
    entry = websearchdict.lookup('a')
    definitions = entry.getDefinitions()
    print(definitions)
    assert {'pos': 'determiner',
            'definition': ('used when referring to someone or something for '
                           'the first time in a text or conversation.'),
            'examples': ['"a man came out of the room"'],
            'synonyms': None} in definitions.values()
    # This is weird, I get 3 locally and GA gets 10 remotely :/
    assert 5 <= len(definitions) <= 9
    assert__pos(definitions)


def test_lookup_define():
    entry = websearchdict.lookup('define')
    definitions = entry.getDefinitions()
    print(definitions)
    assert {'pos': 'verb',
            'definition': ('state or describe exactly the nature, scope, or '
                           'meaning of.'),
            'examples': [('"the contract will seek to define the client\'s '
                          'obligations"')],
            'synonyms': ['explain', 'expound', 'interpret',
                         'elucidate', 'explicate', 'describe', 'clarify',
                         'give the meaning of', 'state precisely',
                         'spell out', 'put into words', 'express in words']
            } in definitions.values()
    assert 2 <= len(definitions) <= 4
    assert__pos(definitions)


def test_lookup_very():
    entry = websearchdict.lookup('very')
    definitions = entry.getDefinitions()
    print(definitions)
    assert {'pos': 'adverb',
            'definition': 'in a high degree.',
            'examples': ['"very much so"'],
            'synonyms': ['extremely', 'exceedingly', 'exceptionally',
                         'especially', 'tremendously', 'immensely', 'vastly',
                         'hugely', 'extraordinarily', 'extra', 'excessively',
                         'overly', 'over', 'abundantly', 'inordinately',
                         'singularly', 'significantly', 'distinctly',
                         'outstandingly', 'uncommonly', 'unusually',
                         'decidedly', 'particularly', 'eminently', 'supremely',
                         'highly', 'remarkably', 'really', 'truly', 'mightily',
                         'thoroughly', 'all that', 'to a great extent', 'most',
                         'so', 'too', 'unco', 'très', 'right', 'terrifically',
                         'awfully', 'terribly', 'devilishly', 'madly',
                         'majorly', 'seriously', 'desperately', 'mega',
                         'ultra', 'oh-so', 'too-too', 'stinking', 'mucho',
                         'damn', 'damned', 'too &#8230; for words', 'devilish',
                         'hellish', 'frightfully', 'ever so', 'well', 'bloody',
                         'dead', 'dirty', 'jolly', 'fair', 'real', 'mighty',
                         'powerful', 'awful', 'plumb', 'darned', 'way',
                         'bitching', 'mad', 'lekker', 'exceeding', 'sore']
            } in definitions.values()
    assert {'pos': 'adjective',
            'definition': ('actual; precise (used to emphasize the exact '
                           'identity of a particular person or thing).'),
            'examples': ['"those were his very words"'],
            'synonyms': ['exact', 'actual', 'precise', 'particular',
                         'specific', 'distinct', 'ideal', 'perfect',
                         'appropriate', 'suitable', 'apt', 'fitting', 'fit',
                         'right', 'just right', 'made to order',
                         'tailor-made', 'spot on', 'just the job']
            } in definitions.values()
    assert 2 <= len(definitions) <= 4
    assert__pos(definitions)


def test_lookup_world():
    entry = websearchdict.lookup('world')
    definitions = entry.getDefinitions()
    assert__pos(definitions)


def test_lookup_or():
    entry = websearchdict.lookup('or')
    definitions = entry.getDefinitions()
    print(definitions)
    assert__pos(definitions)
    assert {'pos': 'conjunction',
            'definition': 'used to link alternatives.',
            'examples': ['"a cup of tea or coffee"',
                         ('"the espionage novel, or, as it is known in the '
                          'trade, the thriller"'),
                         '"hurry up, or you\'ll miss it all"'],
            'synonyms': None} in definitions.values()


def test_lookup_affair_affairs():
    entry = websearchdict.lookup('affair')
    definitions = entry.getDefinitions()
    entry2 = websearchdict.lookup('affairs')
    definitions2 = entry2.getDefinitions()

    assert__pos(definitions)
    assert__pos(definitions2)

    assert 2 == len(definitions) == len(definitions2)


def test_lookup_direct():
    ''' Test that it doesn't accidentally match 'direct' in 'direction' '''
    entry = websearchdict.lookup('direct')
    definitions = entry.getDefinitions()

    print(definitions)
    assert {'pos': 'adjective',
            'definition': ('extending or moving from one place to another by '
                           'the shortest way without changing direction or '
                           'stopping.'),
            'examples': ['"there was no direct flight that day"'],
            'synonyms': ['straight', 'undeviating', 'unswerving', 'shortest',
                         'quickest', 'nonstop', 'unbroken', 'uninterrupted',
                         'straight through', 'through']
            } in definitions.values()
    assert__pos(definitions)

    assert 7 <= len(definitions) <= 11


def test_lookup_be():
    ''' Test that single word definitions are allowed '''
    entry = websearchdict.lookup('be')
    definitions = entry.getDefinitions()

    print(definitions)
    assert {'pos': 'verb',
            'definition': 'exist.',
            'examples': ['"there are no easy answers"'],
            'synonyms': ['exist', 'have being', 'have existence', 'live',
                         'be alive', 'have life', 'breathe', 'draw breath',
                         'be extant', 'be viable']} in definitions.values()
    assert__pos(definitions)


def assert__pos(definitions):
    for sense in definitions:
        assert definitions[sense]['pos'] in wwc.POS_TAGS
