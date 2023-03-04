
import logging
import websearchdict


logging.getLogger("websearchdict").setLevel(logging.DEBUG)

entry = websearchdict.lookup('look', override=True)
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
