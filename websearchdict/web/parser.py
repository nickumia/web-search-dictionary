
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
    examples = ""
    queue = []

    for e in parsed.iter():
        if e.text is not None:
            # print(e.text)
            text_ = e.text.strip().replace('\xa0', '').strip()
            tag_ = e.tag.strip()
            if re.match(wwc.PRONUNCIATION, text_):
                # Pronounciation
                pronounciation += text_ + ' | '
            elif tag_ == 'span' and text_ in wwc.POS_TAGS:
                # POS
                current_pos = text_
            elif '"' in text_:
                # Example
                examples += text_ + ' '
                if text_[-1] != '"':
                    continue
                if text_[-1] == '"':
                    examples = exampleParser(examples)
                    queue.append(examples)
                    examples = ""
            else:
                # Still an example
                if examples != "":
                    examples += text_ + ' '
                    continue
                # Definition
                filtered = notBad(text_, current_pos, target)
                # Check for synonym
                if filtered is not None:
                    if filtered[0:10] == 'synonyms: ':
                        syns = filtered.replace('synonym: ', '')
                        syns = syns.split(', ')
                        queue.append(syns)
                    else:
                        queue.append(current_pos)
                        queue.append(filtered)

    return html.unescape(pronounciation), queueToDict(queue)


def exampleParser(examples):
    examples = set(examples.split('"'))
    try:
        examples.remove('')
        examples.remove(' ')
    except KeyError:
        pass
    return examples


def queueToDict(queue):
    '''
    Definitions always start with a POS Tag.  This function iterates
    through the parsed content and combines elements that are related.
    Possible combinations:
        - pos, definition
        - pos, definition, example
        - pos, definition, example, synonyms
    Example Impossible combinations:
        - pos, definition, synonyms
        - pos, example
        - pos, synonyms
    '''
    definitions = []
    transfer = None

    while len(queue) > 0:
        # Always start with POS
        if transfer is not None:
            items = [transfer]
        else:
            items = [queue.pop(0)]

        # Iterate until the next POS is hit
        current_thing = None
        while current_thing not in wwc.POS_TAGS:
            try:
                current_thing = queue.pop(0)
                if current_thing not in wwc.POS_TAGS:
                    items.append(current_thing)
            except IndexError:
                break
        # Save POS for next time
        transfer = current_thing

        if len(items) == 2:
            definitions.append({
                'pos': items[0],
                'definition': items[1],
                'examples': None,
                'synonyms': None
            })
        elif len(items) == 3:
            definitions.append({
                'pos': items[0],
                'definition': items[1],
                'examples': items[2],
                'synonyms': None
            })
        elif len(items) == 4:
            definitions.append({
                'pos': items[0],
                'definition': items[1],
                'examples': items[2],
                'synonyms': items[3]
            })
    return definitions


def notBad(possible_definition, pos, word):
    rules = []
    results = []

    ''' Question whether the definition should be considered '''

    # Not a generic web blurb
    rules.append((lambda x: x not in wwc.MISC))
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

    if all(results):
        for nonsense in wwc.BAD_PHRASES:
            possible_definition = re.sub(nonsense, '', possible_definition)
        if possible_definition not in ['', ' ']:
            # print(possible_definition)
            # print("_-_-_-_")
            return possible_definition
    return None
