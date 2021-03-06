
from websearchdict.dictionary.entry import Word
from websearchdict.web.fetch import google_search, wiktionary_search
from websearchdict.web.parser import \
    LXML_preprocessHTML, LXML_googleHTML, LXML_wiktionaryHTML


def lookup(word, search=google_search, parser='lxml', override=False):
    A = Word(word)
    web_response = search(word)

    if parser == 'lxml':
        parsed = LXML_preprocessHTML(web_response)
        if search == google_search:
            pronounciation, definitions = LXML_googleHTML(parsed, word,
                                                          web_response.url,
                                                          override=override)
        elif search == wiktionary_search:
            pronounciation, definitions = LXML_wiktionaryHTML(parsed,
                                                              web_response.url,
                                                              override=override
                                                              )

    A.addPronounciation(pronounciation)
    for define in definitions:
        A.addDefinition(define)
    return A
