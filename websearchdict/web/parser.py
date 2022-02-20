
import html
from lxml import etree
import re

import websearchdict.web.constants as wwc
import websearchdict.web.structure as wws
import websearchdict.web.automation as wwsu


def LXML_preprocessHTML(web_response):
    try:
        content = web_response.content.decode("iso-8859-1")
    except AttributeError:
        content = web_response
    # Remove '<!doctype html>' header OR!
    # '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">'
    if content[0:15] == '<!doctype html>':
        content = content[15:]
    elif content[0:63] == ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 '
                           'Transitional//EN">'):
        content = content[63:]

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


def LXML_parseHTML(parsed, target, url):
    pronounciation = ""
    current_pos = None
    queue = []

    if wwsu.checkForLimited(parsed):
        print('Sorry, we\'ve been flagged, trying to complete captcha..')
        parsed = LXML_preprocessHTML(wwsu.backup(url))

    parent = etree.ElementTree(parsed)
    for e in parsed.iter():
        if e.text is not None:
            text_ = e.text.strip().strip() \
                .encode('utf-8').decode('utf-8', 'ignore')
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

    if queue == []:
        return 'none', wwc.ERROR
    return html.unescape(pronounciation), wws.queueToDict(queue)
