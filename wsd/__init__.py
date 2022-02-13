
from wsd.dictionary.entry import Word
from wsd.web.fetch import google_search
from wsd.web.parser import parseHTML, POS_TAGS


MISC = ['G', 'o', 'g', 'l', 'e', 'Videos', 'Please click', 'here', 'All',
        'News', 'Images', 'Videos', 'Maps', 'Shopping', 'Books', '×',
        'Search tools', 'Any time', 'Past hour', 'Past 24 hours', '',
        'Past week', 'Past month', 'Past year', 'All results', 'Verbatim',
        'Related searches', 'Next &gt;', '&nbsp;-&nbsp;', 'Learn more',
        'Sign in', 'Settings', 'Privacy', 'Terms']


def lookup(word):
    A = Word(word)
    web_response = google_search(word)
    parsed = parseHTML(web_response)

    pronounciation = ""
    definitions = []
    current_pos = None

    for e in parsed.iter():
        if e.text is not None:
            text_ = e.text.strip().replace('\xa0', '')
            tag_ = e.tag.strip()
            if '/&#' in text_:
                pronounciation = text_
            elif tag_ == 'span' and text_ in POS_TAGS:
                current_pos = text_
            else:
                if word.lower() not in text_.lower() and text_ not in MISC:
                    definitions.append({
                        'pos': current_pos,
                        'definition': text_
                    })

    A.addPronounciation(pronounciation)
    for define in definitions:
        A.addDefinition(define)
    print(len(definitions))
    return A
