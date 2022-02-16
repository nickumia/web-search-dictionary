
import websearchdict


# Provide acceptable order of the number of definitions
# Varies depending on google search

def test_lookup():
    definitions = websearchdict.lookup('equal')
    # print(definitions.getDefinitions())
    assert definitions.getPronounciation() == '/&#712;&#275;kw&#601;l/'
    assert 6 <= len(definitions.getDefinitions()) <= 10


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
            'examples': {'a man came out of the room'}} in definitions.values()
    assert 3 <= len(definitions) <= 5


def test_lookup_define():
    entry = websearchdict.lookup('define')
    definitions = entry.getDefinitions()
    print(definitions)
    assert {'pos': 'verb',
            'definition': ('state or describe exactly the nature, scope, or '
                           'meaning of.'),
            'examples': {("the contract will seek to define the client's "
                          "obligations")}} in definitions.values()
    assert 4 <= len(definitions) <= 8


def test_lookup_very():
    entry = websearchdict.lookup('very')
    definitions = entry.getDefinitions()
    print(definitions)
    assert {'pos': 'adverb',
            'definition': 'in a high degree.',
            'examples': {'very much so'}} in definitions.values()
    assert {'pos': 'adjective',
            'definition': ('actual; precise (used to emphasize the exact '
                           'identity of a particular person or thing).'),
            'examples': {'those were his very words'}} in definitions.values()
    assert 3 <= len(definitions) <= 7
