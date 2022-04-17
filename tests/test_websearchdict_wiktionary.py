
import websearchdict
import websearchdict.web.structure as wws


# Provide acceptable order of the number of definitions
# Should be more exact with wiktionary

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
    # This is a bit of a problem..
    assert len(definitions) == 428
    assert__pos(definitions)


def test_lookup_world():
    entry = websearchdict.lookup('world')
    definitions = entry.getDefinitions()
    assert len(definitions) == 24
    assert__pos(definitions)


def assert__pos(definitions):
    for sense in definitions:
        assert wws.acceptablePOS(definitions[sense]['pos'])
