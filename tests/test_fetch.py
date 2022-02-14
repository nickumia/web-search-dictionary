
import websearchdict.web.fetch as wwf


def test_google_search():
    response = wwf.google_search('test')
    response.encoding = 'utf-8'

    assert response.status_code == 200
    assert (b'a procedure intended to establish the quality, performance, '
            b'or reliability of something, especially before it is taken into'
            b' widespread use.') in response.content
