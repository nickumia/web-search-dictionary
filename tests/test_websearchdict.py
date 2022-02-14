
import websearchdict


# Provide acceptable order of the number of definitions
# Varies depending on google search

def test_lookup():
    definitions = websearchdict.lookup('equal')
    print(definitions.getDefinitions())
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
    assert {'pos': 'determiner',
            'definition': ('1 : on : in : at abed · 2 : in (such) a state or '
                           'condition afire · 3 : in (such) a manner aloud · '
                           '4 : in the act or process of gone a-hunting ating'
                           'le.')} in definitions.values()
    assert 13 <= len(definitions) <= 17


def test_lookup_define():
    entry = websearchdict.lookup('define')
    definitions = entry.getDefinitions()
    assert {'pos': 'verb',
            'definition': ('state or describe exactly the nature, scope, or '
                           'meaning of.')} in definitions.values()
    assert 11 <= len(definitions) <= 15


def test_lookup_very():
    entry = websearchdict.lookup('very')
    definitions = entry.getDefinitions()
    print(definitions)
    assert {'pos': 'adverb',
            'definition': 'in a high degree.'} in definitions.values()
    assert {'pos': 'adjective',
            'definition': ('actual; precise (used to emphasize the exact '
                           'identity of a particular person or thing).')} \
        in definitions.values()
    assert 8 <= len(definitions) <= 12
