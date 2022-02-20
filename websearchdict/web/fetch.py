
import requests

import websearchdict.web.automation as wwa

session = requests.session()


def google_search(word):
    url = "https://www.%s/search" % (wwa.randomGoogle())
    # url = "https://www.google.com/search"
    print(url)
    payload = {
        'q': 'define ' + word,
    }
    session.cookies.clear()
    r = session.get(url,
                    params=payload,
                    headers=wwa.generateRandomHeaders())

    # print(r.request.headers)
    return r
