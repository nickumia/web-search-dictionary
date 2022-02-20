
import random
import string
import time

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains

import websearchdict.web.constants as wwc

random.seed(time.time())

opts = FirefoxOptions()
opts.add_argument("--headless")
browser = webdriver.Firefox(options=opts)


def generateRandomHeaders():
    headers = {
        # 'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'origin': 'https://www.google.com',
        'connection': 'keep-alive'
    }

    headers['Accept-Language'] = \
        'en-US,en;q=0.%d' % int(random.random() * 10)

    # headers['user-agent'] = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    #                          'AppleWebKit/537.36 (KHTML, like Gecko) '
    #                          'Chrome/98.0.4758.102 Safari/537.36 '
    #                          'Edg/98.0.1108.56')

    return headers


def randomGoogle():
    choice = random.randrange(0, len(wwc.GOOGLES), 1)
    return wwc.GOOGLES[choice]


def checkForLimited(message):
    error = ('In order to continue, please enable javascript on your web '
             'browser.')
    for e in message.iter():
        if e.text is not None:
            text_ = e.text.strip().replace('\xa0', '').strip()
            if text_ == error:
                return True
    return False


def backup(url):
    # print(url)
    browser.get(url)
    # iframes = browser.find_elements_by_tag_name('iframe')
    frame = browser.find_element_by_xpath('//iframe[@title="reCAPTCHA"]')
    browser.switch_to.frame(frame)
    elem = browser.find_element_by_id('recaptcha-anchor')
    click = ActionChains(browser)
    click.click_and_hold(on_element=elem)
    click.perform()
    time.sleep(10)
    click.release(elem)
    time.sleep(3)

    return browser.page_source
