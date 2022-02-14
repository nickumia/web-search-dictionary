
import wsd


def test_lookup():
    definitions = wsd.lookup('equal')
    print(definitions.getDefinitions())
    assert definitions.getPronounciation() == '/&#712;&#275;kw&#601;l/'
    assert len(definitions.getDefinitions()) == 8


def test_example():
    # Get the definitions for 'special'
    entry = wsd.lookup('special')

    # Get the pronounciation for 'special'
    print(entry.getPronounciation())

    # Get the definitions
    for key, sense in entry.getDefinitions().items():
        print('Part of speech [%d]: %s' % (key, sense['pos']))
        print('Definition [%d]: %s' % (key, sense['definition']))
