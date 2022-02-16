
import websearchdict
import sys


if __name__ == '__main__':
    # Get the definitions for input word
    try:
        test = type(sys.argv[1])
    except IndexError:
        print("Please supply a word to lookup "
              "(e.g. 'python example.py world')")
        sys.exit()
    entry = websearchdict.lookup(sys.argv[1])

    # Get the pronounciation for the word
    print(entry.getPronounciation())

    # Get the definitions
    for key, sense in entry.getDefinitions().items():
        print('Part of speech [%d]: %s' % (key, sense['pos']))
        print('Definition [%d]: %s' % (key, sense['definition']))
