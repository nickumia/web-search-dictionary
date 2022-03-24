
import os

import websearchdict.web.parser as wwp


def test_parser():
    cfd = os.path.dirname(os.path.abspath(__file__))

    class TestResponse():
        def __init__(self, content):
            self.content = content
    input_html = TestResponse(open(cfd + '/test.html').read())

    parsed = wwp.LXML_preprocessHTML(input_html.content)

    assert parsed.xpath('/html/head/title')[0].tag == 'title'
    assert parsed.xpath('/html/head/title')[0].text == 'NLP'
    assert parsed.xpath('/html/body')[0].tag == 'body'
    assert parsed.xpath('/html/body')[0].text is None
    assert parsed.xpath('/html/body/h1')[0].text == 'Awesome Test Heading 1'
