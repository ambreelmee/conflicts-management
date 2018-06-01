import requests
import os
import logging


def authenticate():
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    url = (os.getenv('AUTH_URL')+'auth/login?email=' + os.getenv('EMAIL') +
           '&password=' + os.getenv('PASSWORD'))
    r = requests.post(url, proxies=proxyDict)
    if r.status_code == 200:
        logging.info('authentication succeeded')
        return r.json()
    logging.error('authentication failed')
    return None
