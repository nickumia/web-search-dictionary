
from lxml import html


def parseHTML(web_response):
    hdoc = html.fromstring(web_response.content)
    return hdoc
