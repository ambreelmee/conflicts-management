import logging
import requests
import os


def get_link_categories(token):
    url = os.getenv('INSTITUTION_URL')+'link_categories'
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    headers = {'Authorization': 'Bearer ' + token}
    r = requests.get(url, proxies=proxyDict, headers=headers)
    if r.status_code == 200:
        logging.info('link_categories successfully retrieved')
        return r.json()
    else:
        logging.error('unable to get link_categories')


def get_code_categories(token):
    url = os.getenv('INSTITUTION_URL')+'code_categories'
    headers = {'Authorization': 'Bearer ' + token}
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.get(url, proxies=proxyDict, headers=headers)
    if r.status_code == 200:
        logging.info('code_categories successfully retrieved')
        return r.json()
    else:
        logging.error('unable to get code_categories')


def get_institution_from_esr(uai_number):
    url = (os.getenv('INSTITUTION_URL')+'codes/search?q=' + uai_number +
           '&status=active')
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(url, proxies=proxyDict)
    if r.status_code == 200:
        if 'message' in r.json().keys():
            logging.debug('%s:  institution not found in dataESR', uai_number)
            return None
        return r.json()
    return None
