
from lxml import etree
import re


POS_TAGS = [
    'noun',
    'adjective',
    'verb',
    'determiner'
]

MISC = ['G', 'o', 'g', 'l', 'e', 'Videos', 'Please click', 'here', 'All',
        'News', 'Images', 'Videos', 'Maps', 'Shopping', 'Books', '×',
        'Search tools', 'Any time', 'Past hour', 'Past 24 hours', '',
        'Past week', 'Past month', 'Past year', 'All results', 'Verbatim',
        'Related searches', 'Next &gt;', '&nbsp;-&nbsp;', 'Learn more',
        'Sign in', 'Settings', 'Privacy', 'Terms', 'People also ask',
        'See results about', '·', 'More results', 'Best dictionary website',
        'Duration:']


def LXML_preprocessHTML(web_response):
    if type(web_response.content) == str:
        hdoc = etree.fromstring(web_response.content)
    else:
        content = web_response.content.decode("iso-8859-1")
        # Remove '<!doctype html>' header
        content = content[15:]
        # Combine into one line
        content = ' '.join(content.split('\n'))
        # Make html safe
        content = content.replace('&', '&amp;')
        content = content.replace('<=', '&lt;=')
        # Ignore all (style|img|br|script|comment|meta|input) tags.
        content = re.sub(r'<style>.*?</style>', '', content,
                         flags=re.I | re.M | re.U)
        content = re.sub(r'<img .*?">', '', content)
        content = re.sub(r'<input .*?">', '', content)
        content = re.sub(r'<br>', '', content)
        content = re.sub(r'<([a-z]|[A-Z])(\[[0-9]+\])?\.length',
                         '&lt;a.length', content)
        content = re.sub(r'<script.*?</script>', '', content)
        content = re.sub(r'<!--.*?-->', '', content)
        content = re.sub(r'<meta .*?">', '', content)

        # TODO: Fix timing of this replacement
        content = re.sub(r'[0-9]+ days ago', '', content)
        # print(content)
        hdoc = etree.fromstring(content)
    return hdoc


def LXML_parseHTML(parsed, target):
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
                filtered = notBad(text_, current_pos, target)
                if filtered is not None:
                    definitions.append({
                        'pos': current_pos,
                        'definition': filtered
                    })
    return pronounciation, definitions


def notBad(possible_definition, pos, word):
    rules = []
    results = []

    ''' Question whether the definition should be considered '''

    # Not a generic web blurb
    rules.append((lambda x: x not in MISC))
    rules.append((lambda x, y: y.lower() not in x.lower()))

    for rule in rules:
        try:
            results.append(rule(possible_definition))
        except TypeError:
            if pos != 'determiner':
                # Word should not define itself
                results.append(rule(possible_definition, word))
            results.append(rule(possible_definition, 'define'))

    ''' Postprocessing to weed out null results '''
    bad_phrases = [
        r'Define ([a-z]|[A-z])+( .*)?',
        r'How to pronounce ([a-z]|[A-z])+',
        r'Example of ([a-z]|[A-z])+( .*)?',
        r'(Merriam-Webster|Vocabulary\.com|Dictionary(\.com)?|'
        r'Purdue Online Writing Lab|Merriam...|Urban|Webster\'s|'
        r'Cambridge Advanced...|Best dictionary website)',
        r'([a-z]|[A-Z]){3} [0-9]{2}, [0-9]{4}',
        r'[0-9]{1,2}:[0-9]{2}',
        r'(A Definition)? &amp; Meaning (-|\|) ',
        r'.*&#8250;.*',
    ]

    if all(results):
        for nonsense in bad_phrases:
            possible_definition = re.sub(nonsense, '', possible_definition)
        if possible_definition not in ['', ' ']:
            print(possible_definition)
            print("_-_-_-_")
            return possible_definition
    return None
