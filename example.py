
import websearchdict
from websearchdict.web.fetch import google_search, wiktionary_search
import sys

# SEARCH = 'wiktionary'
SEARCH = 'google'

if __name__ == '__main__':
    # Get the definitions for input word
    try:
        test = type(sys.argv[1])
    except IndexError:
        print("Please supply a word to lookup "
              "(e.g. 'python example.py world')")
        sys.exit()

    if SEARCH == 'google':
        entry = websearchdict.lookup(sys.argv[1], search=google_search)
    elif SEARCH == 'wiktionary':
        entry = websearchdict.lookup(sys.argv[1], search=wiktionary_search)

    # Get the pronounciation for the word
    print(entry.getPronounciation())

    # Get the definitions
    for key, sense in entry.getDefinitions().items():
        print('Part of speech [%d]: %s' % (key, sense['pos']))
        print('Definition [%d]: %s' % (key, sense['definition']))
        try:
            for example in sense['examples']:
                print('Example [%d]: %s' % (key, example))
        except TypeError:
            print('Example [%d]: %s' % (key, sense['examples']))
        print('Synonyms [%d]: %s' % (key, sense['synonyms']))
