
import html
import re

import websearchdict.web.constants as wwc
import websearchdict.web.parser as wwp


def LXML_parseHTML(parsed, target):
    pronounciation = ""
    current_pos = None
    examples = ""
    queue = []

    for e in parsed.iter():
        if e.text is not None:
            # print("|" + e.text + "|")
            text_ = e.text.strip().replace('\xa0', '').strip()
            tag_ = e.tag.strip()
            # print("|" + text_ + "|")
            # print("|" + tag_ + "|")
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
                filtered = wwp.notBad(text_, current_pos, target)
                # Check for synonym
                if filtered is not None and current_pos is not None:
                    if filtered[0:10] == 'synonyms: ':
                        syns = filtered.replace('synonyms: ', '')
                        syns = syns.split(', ')
                        queue.append(syns)
                    else:
                        queue.append(current_pos)
                        queue.append(filtered)

    return html.unescape(pronounciation), wwp.queueToDict(queue)


def exampleParser(examples):
    examples = set(examples.split('"'))
    try:
        examples.remove('')
        examples.remove(' ')
    except KeyError:
        pass
    return examples
