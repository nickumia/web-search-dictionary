
from websearchdict.dictionary.entry import Word
from websearchdict.web.fetch import google_search
from websearchdict.web.parser import \
    LXML_preprocessHTML, LXML_parseHTML


def lookup(word, parser='lxml', override=False):
    A = Word(word)
    web_response = google_search(word)

    if parser == 'lxml':
        parsed = LXML_preprocessHTML(web_response)
        pronounciation, definitions = LXML_parseHTML(parsed, word,
                                                     web_response.url,
                                                     override=override)

    A.addPronounciation(pronounciation)
    for define in definitions:
        A.addDefinition(define)
    return A
