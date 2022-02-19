
import html
from lxml import etree
import re

import websearchdict.web.constants as wwc
import websearchdict.web.structure as wws


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

        print(content)
        hdoc = etree.fromstring(content)
    return hdoc


def LXML_parseHTML(parsed, target):
    pronounciation = ""
    current_pos = None
    queue = []

    parent = etree.ElementTree(parsed)
    for e in parsed.iter():
        if e.text is not None:
            text_ = e.text.strip().replace('\xa0', '').strip()
            tag_ = e.tag.strip()
            p_ = parent.getpath(e)
            # print("|" + text_ + "|")
            # print("|" + tag_ + "|")
            # print(parent.getpath(e),)
            if re.match(wwc.PRONUNCIATION, text_):
                # Pronounciation
                pronounciation += text_ + ' | '
            elif tag_ == 'span' and wws.acceptablePOS(text_):
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
                        filtered = wws.notBad(text_, current_pos, target,
                                              example=True)
                        if filtered is not None and current_pos is not None \
                           and len(queue) > 0:
                            queue.append((wwc.ID_EXAMPLE, filtered))
            elif tag_ == 'div' and '/a/' not in p_:
                # Definition
                filtered = wws.notBad(text_, current_pos, target)
                if filtered is not None and current_pos is not None:
                    queue.append((wwc.ID_POS, current_pos))
                    queue.append((wwc.ID_DEFINITION, filtered))

    return html.unescape(pronounciation), wws.queueToDict(queue)
