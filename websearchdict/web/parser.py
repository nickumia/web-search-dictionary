
import html
from lxml import etree
import re


POS_TAGS = [
    'noun',
    'adjective',
    'verb',
    'adverb',
    'determiner'
]

MISC = ['G', 'o', 'g', 'l', 'e', 'Videos', 'Please click', 'here', 'All',
        'News', 'Images', 'Videos', 'Maps', 'Shopping', 'Books', '×',
        'Search tools', 'Any time', 'Past hour', 'Past 24 hours', '',
        'Past week', 'Past month', 'Past year', 'All results', 'Verbatim',
        'Related searches', 'Next &gt;', '&nbsp;-&nbsp;', 'Learn more',
        'Sign in', 'Settings', 'Privacy', 'Terms', 'People also ask',
        'See results about', '·', 'More results', 'Best dictionary website',
        'Duration:', 'Rating', 'View all']


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
    re_pronounce = r'/(&#|[a-z}|[A-Z]|[0-9]|;|,)+/'
    definitions = []
    current_pos = None
    examples = ""
    still_example = False
    queue = []

    for e in parsed.iter():
        if e.text is not None:
            # print(e.text)
            text_ = e.text.strip().replace('\xa0', '').strip()
            tag_ = e.tag.strip()
            if re.match(re_pronounce, text_):
                # Pronounciation
                pronounciation += text_ + ' | '
            elif tag_ == 'span' and text_ in POS_TAGS:
                # POS
                current_pos = text_
            elif '"' in text_:
                # Example
                examples += text_ + ' '
                if text_[-1] != '"':
                    still_example = True
                    continue
                if text_[-1] == '"':
                    still_example = False
                    examples = exampleParser(examples)
                    queue.append(examples)
                    examples = ""
            else:
                if still_example:
                    examples += text_ + ' '
                    continue
                # Definition
                filtered = notBad(text_, current_pos, target)
                if filtered is not None:
                    queue.append(current_pos)
                    queue.append(filtered)

    pos = None
    fed = None
    exa = None
    while len(queue) > 0:
        current_thing = queue.pop(0)
        if pos is None:
            pos = current_thing
        elif fed is None:
            fed = current_thing
        elif exa is None:
            if type(current_thing) == set:
                exa = current_thing
                definitions.append({
                    'pos': pos,
                    'definition': fed,
                    'examples': exa
                })
                pos = None
            else:
                definitions.append({
                    'pos': pos,
                    'definition': fed,
                    'examples': exa
                })
                pos = current_thing
            fed = None
            exa = None

    return html.unescape(pronounciation), definitions


def exampleParser(examples):
    try:
        examples = set(examples.split('"'))
        try:
            examples.remove('')
            examples.remove(' ')
        except KeyError:
            pass
    except TypeError:
        examples = ["None."]
    return examples


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
        r'([a-z]|[A-z])+ definition',
        r'Definition of ([a-z]|[A-z])+(.*)?',
        r'How to pronounce ([a-z]|[A-z])+',
        r'Example of ([a-z]|[A-z])+( .*)?',
        r'(Merriam-Webster|Vocabulary\.com|(Best English )?Dictionary(\.com)?|'
        r'Purdue Online Writing Lab|Merriam...|Urban|Webster\'s|'
        r'Cambridge Advanced...|Best dictionary website|In stock|'
        r'Wikipedia|Noun:?|Collins English Di...|Past participle:|'
        r'Adverb and Its Kinds|Adjective:?|Verb:?|Oxford English Di...)',
        r'([a-z]|[A-Z]){3} [0-9]{1,2}, [0-9]{4}',
        r'[0-9]{1,2}:[0-9]{2}',
        r'(A Definition)? &amp; Meaning (-|\|) ',
        r'(\$?[0-9]+\.[0-9]{1,2}|\([0-9]+\)|^[0-9]$)',
        r'.*&#; Best Sellers &#;.*',
        r'.*&#8250;.*',
        r'.*?\?',
    ]

    if all(results):
        for nonsense in bad_phrases:
            possible_definition = re.sub(nonsense, '', possible_definition)
        if possible_definition not in ['', ' ']:
            # print(possible_definition)
            # print("_-_-_-_")
            return possible_definition
    return None
