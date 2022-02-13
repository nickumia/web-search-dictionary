
from lxml import etree
import re


def parseHTML(web_response):
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
        # print(content)
        hdoc = etree.fromstring(content)
    return hdoc


POS_TAGS = [
    'noun',
    'adjective',
    'verb'
]
