
import requests

import websearchdict.web.automation as wwa

session = requests.session()


def google_search(word):
    '''
    Lookup the word with the google search engine
    - Currently, only english words are supported.
    '''
    url = "https://www.%s/search?hl=en" % (wwa.randomGoogle())
    print("Query url: %s" % (url))
    payload = {
        'q': 'define ' + word,
    }
    session.cookies.clear()
    r = session.get(url,
                    params=payload,
                    headers=wwa.generateRandomHeaders())

    if r.status_code == 200:
        return r
    elif r.status_code == 429:
        print('The request was rate-limited :(')
        return error("<!doctype html> <error></error>")
    else:
        print('Code %d: %s' % (r.status_code, r.text))
        return error("<!doctype html> <error></error>")


def wiktionary_search(word):
    '''
    Lookup the word using wiktionary's search engine
    '''
    url = "https://en.wiktionary.org/wiki/%s" % (word)

    session.cookies.clear()
    r = session.get(url,
                    headers=wwa.generateRandomHeaders())

    if r.status_code == 200:
        return r
    elif r.status_code == 429:
        print('The request was rate-limited :(')
        return error("<!doctype html> <error></error>")
    else:
        print('Code %d: %s' % (r.status_code, r.text))
        return error("<!doctype html> <error></error>")


class error(str):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.url = "kamutiv.com"
