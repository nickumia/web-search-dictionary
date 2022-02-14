
from lxml import etree
import re


POS_TAGS = [
    'noun',
    'adjective',
    'verb'
]

MISC = ['G', 'o', 'g', 'l', 'e', 'Videos', 'Please click', 'here', 'All',
        'News', 'Images', 'Videos', 'Maps', 'Shopping', 'Books', '×',
        'Search tools', 'Any time', 'Past hour', 'Past 24 hours', '',
        'Past week', 'Past month', 'Past year', 'All results', 'Verbatim',
        'Related searches', 'Next &gt;', '&nbsp;-&nbsp;', 'Learn more',
        'Sign in', 'Settings', 'Privacy', 'Terms', 'People also ask',
        'See results about', '·']


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
                if target.lower() not in text_.lower() and text_ not in MISC:
                    definitions.append({
                        'pos': current_pos,
                        'definition': text_
                    })
    return pronounciation, definitions
