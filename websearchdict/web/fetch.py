
import requests
from torpy.http.requests import TorRequests
import urllib3

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


def tor_search(word):
    url = "https://www.google.com/search"
    payload = {
        'q': 'define ' + word,
    }

    # Courtesy of https://medium.com/geekculture/rotate-ip-address-and-user-agent-to-scrape-data-a010216c8d0c  NOQA
    with TorRequests() as tor_requests:
        with tor_requests.get_session() as sess:
            print(sess.get("http://httpbin.org/ip").json())
            response = sess.get(url,
                                params=payload)

    return response.text

