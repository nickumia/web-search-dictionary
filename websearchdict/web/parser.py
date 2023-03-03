
import html
import logging
from lxml import etree
import re

import websearchdict.web.constants as wwc
import websearchdict.web.structure as wws
import websearchdict.web.automation as wwsu


logger = logging.getLogger(__name__)


def LXML_preprocessHTML(web_response):
    logging.debug('Content from LXML_preprocessHTML')
    try:
        # UTF8 is preferred for wiktionary
        # iso-8859-1 is preferred for google
        content = web_response.content.decode("iso-8859-1")
    except AttributeError:
        content = web_response

    # Remove '<!doctype html>' header OR!
    # '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">'
    if content[0:15].lower() == '<!doctype html>':
        content = content[15:]
    elif content[0:63].lower() == ('<!doctype html public "-//w3c//dtd html '
                                   '4.01 transitional//en">'):
        content = content[63:]

    # Combine into one line
    content = ' '.join(content.splitlines())
    # Make html safe
    content = content.replace('&', '&amp;')
    content = content.replace('<=', '&lt;=')
    # '<' '>' signs in JS code sucks..
    content = re.sub(r'<([a-z]|[A-Z])(\[[0-9]+\])?\.length',
                     '&lt;a.length', content)
    # Ignore all (style|img|br|script|comment|meta|input|hr) tags.
    for unsafe_tag in wwc.BAD_TAGS:
        content = re.sub(unsafe_tag, '', content)

    logging.debug(content)
    hdoc = etree.fromstring(content)
    return hdoc


def LXML_googleHTML(parsed, target, url, override=False):
    pronounciation = ""
    current_pos = None
    queue = []

    if wwsu.checkForLimited(parsed):
        logging.warning('We\'ve been flagged! :( trying to complete captcha..')
        parsed = LXML_preprocessHTML(wwsu.backup(url, override=override))

    parent = etree.ElementTree(parsed)
    for e in parsed.iter():
        if e.text is not None:
            text_ = e.text.strip().strip() \
                .encode('utf-8').decode('utf-8', 'ignore')
            tag_ = e.tag.strip()
            p_ = parent.getpath(e)
            logging.debug("| %s |", text_)
            logging.debug("| %s |", tag_)
            logging.debug(parent.getpath(e))
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
            elif tag_ == 'div' and not re.match(wwc.LINK, p_):
                # Definition
                filtered = wws.notBad(text_, current_pos, target)
                if filtered is not None and current_pos is not None:
                    queue.append((wwc.ID_POS, current_pos))
                    queue.append((wwc.ID_DEFINITION, filtered))

    if queue == []:
        return 'none', wwc.ERROR
    return html.unescape(pronounciation), wws.queueToDict(queue)


def LXML_wiktionaryHTML(parsed, url, override=False):
    pronounciation = ""
    current_pos = None
    queue = []

    if wwsu.checkForLimited(parsed):
        logging.warning('We\'ve been flagged! :( trying to complete captcha..')
        parsed = LXML_preprocessHTML(wwsu.backup(url, override=override))

    parent = etree.ElementTree(parsed)
    for e in parsed.iter():
        if e.tag.strip() == 'span':
            if re.match(r'h3\[[0-9]+\]', parent.getpath(e).split('/')[-2]):
                # POS
                if e.text is not None:
                    text_ = e.text.strip().strip() \
                        .encode('utf-8').decode('utf-8', 'ignore')
                    if wws.acceptablePOS(text_):
                        current_pos = text_
        if e.tag.strip() == 'span':
            if e.get('class') == 'IPA':
                # Pronounciation
                if e.text is not None:
                    text_ = e.text.strip().encode('utf8')
                    text_ = text_.replace(b'\x9c', b'')
                    text_ = text_.replace(b'\x90', b'')
                    text_ = text_.replace(b'\x9d', b'')
                    text_ = text_.replace(b'\x9b', b'')
                    # text_ = re.sub(r'\\x[a-f0-9]{2}', '', text_)
                    pronounciation += text_.decode('utf-8', 'ignore') + ' | '
        elif e.tag.strip() == 'ol':
            # List of definitions for preceding POS
            definitions = LXML_definition_ol(e)
            for define in definitions:
                queue.append((wwc.ID_POS, current_pos))
                queue.append((wwc.ID_DEFINITION, define))

    return pronounciation, wws.queueToDict(queue, one_more=True)


def LXML_definition_ol(e):
    '''
    Parse a block of definitions per a particular POS
    Basic structure: an ordered list with the top-level information
        being the definition.  There are sub-tags and sub-bullets
        that hold more information, such as history, examples and
        synonyms
    IN: XML Tree (starting with 'ol' tag)
    OUT: List of definitions
    '''
    tex = []
    number = None
    definition = ' '
    parent = etree.ElementTree(e)
    for f in e.iter():
        root = parent.getpath(f).split('/')[-2] == 'ol'
        item = parent.getpath(f).split('/')[-1].split('[')[0] == 'li'
        try:
            numb = parent.getpath(f).split('[')[1].split(']')[0]
        except IndexError:
            numb = '-1'
        if all([root, item]):
            if numb != number:
                number = numb
                if definition.strip() != '':
                    tex.append((definition.strip()))
                definition = ' '

        # TODO: extract examples, synonyms, etc
        if 'dl' in parent.getpath(f):
            continue
        if 'ul' in parent.getpath(f):
            continue

        if isinstance(f.text, str):
            definition += f.text + ' '
        if isinstance(f.tail, str):
            definition += f.tail + ' '

    tex.append((definition))
    return tex
