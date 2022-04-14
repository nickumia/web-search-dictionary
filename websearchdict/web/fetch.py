
import requests

import websearchdict.web.automation as wwa

session = requests.session()


def google_search(word):
    '''
    Lookup the word with the google search engine
    - Currently, only english words are supported.
    '''
    url = "https://www.%s/search?hl=en" % (wwa.randomGoogle())
    # url = "https://www.google.com/search"
    print("Query url: %s" % (url))
    payload = {
        'q': 'define ' + word,
    }
    session.cookies.clear()
    r = session.get(url,
                    params=payload,
                    headers=wwa.generateRandomHeaders())

    # print(r.request.headers)
    return r


def wiktionary_search(word):
    '''
    Lookup the word using wiktionary's search engine
    '''
    url = "https://en.wiktionary.org/wiki/%s" % (word)

    session.cookies.clear()
    r = session.get(url,
                    headers=wwa.generateRandomHeaders())
    return r
