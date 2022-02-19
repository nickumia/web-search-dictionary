
import html
from lxml import etree
import re

import websearchdict.web.constants as wwc


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
        # '<' '>' signs in JS code sucks..
        content = re.sub(r'<([a-z]|[A-Z])(\[[0-9]+\])?\.length',
                         '&lt;a.length', content)
        # Ignore all (style|img|br|script|comment|meta|input|hr) tags.
        for unsafe_tag in wwc.BAD_TAGS:
            content = re.sub(unsafe_tag, '', content)

        # print(content)
        hdoc = etree.fromstring(content)
    return hdoc


def LXML_parseHTML(parsed, target):
    pronounciation = ""
    current_pos = None
    queue = []

    parent = etree.ElementTree(parsed)
    for e in parsed.iter():
        if e.text is not None:
            # print("|" + e.text + "|")
            text_ = e.text.strip().replace('\xa0', '').strip()
            tag_ = e.tag.strip()
            p_ = parent.getpath(e)
            # print("|" + text_ + "|")
            # print("|" + tag_ + "|")
            # print(parent.getpath(e),)
            if re.match(wwc.PRONUNCIATION, text_):
                # Pronounciation
                pronounciation += text_ + ' | '
            elif tag_ == 'span' and text_ in wwc.POS_TAGS:
                # POS
                current_pos = text_
            elif tag_ == 'span':
                # Examples | Synonyms
                if text_[0:10] == 'synonyms: ':
                    syns = text_.replace('synonyms: ', '')
                    syns = syns.split(', ')
                    queue.append((wwc.ID_SYNONYM, syns))
                else:
                    # TODO: watch out for this changing
                    if not re.match(wwc.MARKETING, p_):
                        filtered = notBad(text_, current_pos, target,
                                          example=True)
                        if filtered is not None and current_pos is not None:
                            queue.append((wwc.ID_EXAMPLE, filtered))
            elif tag_ == 'div' and '/a/' not in p_:
                # Definition
                filtered = notBad(text_, current_pos, target)
                if filtered is not None and current_pos is not None:
                    queue.append((wwc.ID_POS, current_pos))
                    queue.append((wwc.ID_DEFINITION, filtered))

    return html.unescape(pronounciation), queueToDict(queue)


def queueToDict(queue):
    '''
    All items are tagged with what type of data it is,
    - POS
    - DEFINITION
    - EXAMPLE
    - SYNONYM

    This groups the items in the list accordingly.  Groups always begin
    with a POS.
    '''
    definitions = []
    pos = None
    fed = None
    exa = []
    syn = None

    while len(queue) > 0:
        # Always start with POS
        if pos is None:
            pos = queue.pop(0)[1]

        if queue[0][0] != wwc.ID_POS:
            current_thing = queue.pop(0)
            if current_thing[0] == wwc.ID_DEFINITION:
                fed = current_thing[1]
            elif current_thing[0] == wwc.ID_EXAMPLE:
                exa.append(current_thing[1])
            elif current_thing[0] == wwc.ID_SYNONYM:
                syn = current_thing[1]
        else:
            # Summary results in entry
            definitions.append({
                'pos': pos,
                'definition': fed,
                'examples': exa,
                'synonyms': syn
            })
            pos = None
            exa = []
            syn = None
    return definitions


def notBad(possible_definition, pos, word, example=False):
    rules = []
    results = []

    ''' Question whether the definition should be considered '''

    # Not a generic web blurb
    rules.append((lambda x: x not in wwc.MISC))
    # Not a POS
    # rules.append((lambda x: len(x.strip().split(' ')) > 1))
    rules.append((lambda x: x.strip().lower() not in wwc.POS_TAGS))

    for rule in rules:
        try:
            results.append(rule(possible_definition))
        except TypeError:
            if pos != 'determiner':
                # Word should not define itself
                results.append(rule(possible_definition, word))
                # TODO: Ignore lemmas
                if word[-1] == 's':
                    results.append(rule(possible_definition, word[0:-1]))
            results.append(rule(possible_definition, 'define'))
    # print(results)

    ''' Postprocessing to weed out null results '''

    if all(results):
        for nonsense in wwc.BAD_PHRASES:
            possible_definition = re.sub(nonsense, '', possible_definition)
        if possible_definition not in ['', ' ']:
            # print(possible_definition)
            # print("_-_-_-_")
            return possible_definition
    return None

# a = 'secondhand.'
# print(notBad(a, 'asdf', 'used'))
