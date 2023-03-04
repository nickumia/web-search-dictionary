
import websearchdict
import websearchdict.web.structure as wws
from websearchdict.web.fetch import google_search


# Provide acceptable order of the number of definitions
# Varies depending on google search

def test_lookup():
    definitions = websearchdict.lookup('equal', search=google_search)
    # print(definitions.getDefinitions())
    assert any(
        [definitions.getPronounciation() == '/ˈēkwəl/ | ',
         definitions.getPronounciation() == '/ËÄkwÉl/ | ',
         definitions.getPronounciation() == '/ˈēkw(ə)l/ | ',
         definitions.getPronounciation().encode('utf8') == b'/\xc3\x8b\xc2\x88\xc3\x84\xc2\x93kw\xc3\x89\xc2\x99l/ | ',  # NOQA
         definitions.getPronounciation() == '/ˈçkwəl/ | ']
    )
    assert 8 <= len(definitions.getDefinitions()) <= 12
    assert__pos(definitions.getDefinitions())


def test_example():
    # Get the definitions for 'special'
    entry = websearchdict.lookup('special', search=google_search)

    # Get the pronounciation for 'special'
    print(entry.getPronounciation())

    # Get the definitions
    for key, sense in entry.getDefinitions().items():
        print('Part of speech [%d]: %s' % (key, sense['pos']))
        print('Definition [%d]: %s' % (key, sense['definition']))


def test_lookup_a():
    entry = websearchdict.lookup('a', search=google_search)
    definitions = entry.getDefinitions()
    print(definitions)
    assert {'pos': 'determiner',
            'definition': ('used when referring to someone or something for '
                           'the first time in a text or conversation.'),
            'examples': ['"a man came out of the room"'],
            'synonyms': None} in definitions.values()
    assert 8 <= len(definitions) <= 11
    assert__pos(definitions)


def test_lookup_define():
    entry = websearchdict.lookup('define', search=google_search)
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
    assert 8 <= len(definitions) <= 12
    assert__pos(definitions)


def test_lookup_very():
    entry = websearchdict.lookup('very', search=google_search)
    definitions = entry.getDefinitions()
    print(definitions)
    assert definitions[0]['pos'] == 'adverb'
    assert definitions[0]['definition'] == 'in a high degree.'
    assert definitions[0]['examples'] == ['"very much so"']
    assert definitions[0]['synonyms'][0] == 'extremely'
    assert definitions[0]['synonyms'][1] == 'exceedingly'
    assert definitions[0]['synonyms'][2] == 'exceptionally'
    assert definitions[0]['synonyms'][3] == 'especially'
    assert definitions[0]['synonyms'][-1] == 'sore'
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
    assert 8 <= len(definitions) <= 12
    assert__pos(definitions)


def test_lookup_world():
    entry = websearchdict.lookup('world', search=google_search)
    definitions = entry.getDefinitions()
    assert__pos(definitions)


def test_lookup_or():
    entry = websearchdict.lookup('or', search=google_search)
    definitions = entry.getDefinitions()
    print(definitions)
    assert__pos(definitions)
    assert {'pos': 'conjunction',
            'definition': 'used to link alternatives.',
            'examples': ['"a cup of tea or coffee"'],
            'synonyms': None} in definitions.values()


def test_lookup_affair_affairs():
    entry = websearchdict.lookup('affair', search=google_search)
    definitions = entry.getDefinitions()
    entry2 = websearchdict.lookup('affairs', search=google_search)
    definitions2 = entry2.getDefinitions()

    assert__pos(definitions)
    assert__pos(definitions2)

    # The following can no longer be guaranteed
    assert len(definitions) == len(definitions2) + 2

    # This is apparently true sometimes..
    # assert len(definitions) < len(definitions2)
    assert len(definitions2) < 20


def test_lookup_direct():
    ''' Test that it doesn't accidentally match 'direct' in 'direction' '''
    entry = websearchdict.lookup('direct', search=google_search)
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

    assert 13 <= len(definitions) <= 17


def test_lookup_be():
    ''' Test that single word definitions are allowed '''
    entry = websearchdict.lookup('be', search=google_search)
    definitions = entry.getDefinitions()

    print(definitions)
    assert {'pos': 'verb',
            'definition': 'exist.',
            'examples': ['"there are no easy answers"'],
            'synonyms': ['exist', 'have being', 'have existence', 'live',
                         'be alive', 'have life', 'breathe', 'draw breath',
                         'be extant', 'be viable']} in definitions.values()
    assert__pos(definitions)


def test_lookup_used():
    ''' Test that definitions are allowed to have the word in them  '''
    entry = websearchdict.lookup('used', search=google_search)
    definitions = entry.getDefinitions()

    print(definitions)
    assert {'pos': 'adjective',
            'definition': 'having already been used.',
            'examples': ['"scrawling on the back of a used envelope"'],
            'synonyms': None} in definitions.values()
    assert__pos(definitions)


def test_lookup_all():
    ''' Test that allows multiple POS tags in a single definition  '''
    entry = websearchdict.lookup('all', search=google_search)
    definitions = entry.getDefinitions()

    print(definitions)
    assert {'pos': 'predeterminer, determiner, pronoun',
            'definition': ('used to refer to the whole quantity or extent of a'
                           ' particular group or thing.'),
            'examples': ['"all the people I met"'],
            'synonyms': ['each of', 'each one of the', 'every one of the',
                         'every single one of the', 'every', 'each and every',
                         'every single', 'the whole of the',
                         'every bit of the', 'the complete', 'the entire',
                         'the totality of the', 'in its entirety', 'complete',
                         'entire', 'total', 'full', 'utter', 'perfect',
                         'all-out', 'greatest (possible)', 'maximum',
                         'everyone', 'everybody', 'each/every person',
                         'the (whole) lot', 'each one', 'each thing',
                         'the sum', 'the total', 'the whole lot', 'everything',
                         'every part', 'the whole amount', 'the total amount',
                         'the entirety', 'the sum total', 'the aggregate']
            } in definitions.values()
    assert__pos(definitions)


def test_lookup_visible():
    ''' This word seems to fail reliably outside of this repo..so tests '''
    entry = websearchdict.lookup('visible', search=google_search)
    definitions = entry.getDefinitions()

    print(definitions)
    assert__pos(definitions)


def assert__pos(definitions):
    for sense in definitions:
        assert wws.acceptablePOS(definitions[sense]['pos'])
