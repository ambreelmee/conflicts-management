import requests
import os
import logging


def authenticate():
    logging.info('########### AUTHENTICATE ############')
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    url = (os.getenv('AUTH_URL')+'auth/login?email=' + os.getenv('EMAIL') +
           '&password=' + os.getenv('PASSWORD'))
    r = requests.post(url, proxies=proxyDict)
    logging.info(url)
    if r.status_code == 200:
        logging.info('authentication succeeded')
        logging.info(r.json())
        return r.json()['access_token']
    logging.info('authentication failed')
    return None
