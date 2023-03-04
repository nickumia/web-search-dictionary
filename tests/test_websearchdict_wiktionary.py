
import websearchdict
import websearchdict.web.structure as wws
from websearchdict.web.fetch import wiktionary_search


# Provide acceptable order of the number of definitions
# Should be more exact with wiktionary

def test_lookup():
    definitions = websearchdict.lookup('world', search=wiktionary_search)
    # print(definitions.getDefinitions())
    assert definitions.getPronounciation() == \
        ('/wÉËld/ | /wÉld/ | /wÉµËld/ | [wÉµËÉ¯Ì¯dÌ¥] | '
         '-ÉË(É¹)ld | /wurld/ | /wÉrld/ | ')

    assert len(definitions.getDefinitions()) == 24
    assert__pos(definitions.getDefinitions())


def test_example():
    # Get the definitions for 'special'
    entry = websearchdict.lookup('special', search=wiktionary_search)

    # Get the pronounciation for 'special'
    print(entry.getPronounciation())

    # Get the definitions
    for key, sense in entry.getDefinitions().items():
        print('Part of speech [%d]: %s' % (key, sense['pos']))
        print('Definition [%d]: %s' % (key, sense['definition']))


def test_lookup_a():
    entry = websearchdict.lookup('a', search=wiktionary_search)
    definitions = entry.getDefinitions()
    print(definitions)
    # This is a bit of a problem..
    assert len(definitions) == 506
    assert__pos(definitions)


def assert__pos(definitions):
    for sense in definitions:
        assert wws.acceptablePOS(definitions[sense]['pos'])
