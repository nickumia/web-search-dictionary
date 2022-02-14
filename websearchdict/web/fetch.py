
import requests


def google_search(word):
    url = "https://www.google.com/search"
    payload = {
        'q': 'define ' + word,
    }
    # headers = {
    #     'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
    #                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.'
    #                    '0.2171.95 Safari/537.36')
    # }
    # return requests.get(url, params=payload, headers=headers)
    return requests.get(url, params=payload)
