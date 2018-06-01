import logging
import requests
import os
from .constants import public_prive_dict, ministere_dict, cat_juridiques_dict
from repositories import DatabaseConnectionRepository


def find_category_id(categories_list, bce_field):
    # find category_name from bce_field
    connections = DatabaseConnectionRepository.get(bce_field=bce_field)
    category_name = connections.criterion_value
    return next((category['id'] for category in categories_list
                if category['title'] == category_name), None)


def create_esr_institution(token, numero_uai, sigle_uai, patronyme_uai,
                           date_ouverture, date_fermeture,
                           numero_siren_siret_uai, adresse_uai,
                           boite_postale_uai, code_postal_uai,
                           localite_acheminement_uai, numero_telephone_uai,
                           secteur_public_prive, ministere_tutelle,
                           categorie_juridique, site_web, link_categories,
                           code_categories, count):

    # some institutions have no 'sigle_uai' or no 'patronyme_uai'
    # but field 'name' and 'initials' are mandatory in dataESR
    # if one is null then both fields have the same value
    data = {'institution':
            {'name': patronyme_uai if patronyme_uai else sigle_uai,
             'initials': sigle_uai if sigle_uai else patronyme_uai,
             'date_start': str(date_ouverture),
             'date_end': str(date_fermeture)}}
    url = os.getenv('INSTITUTION_URL')+'institutions'
    headers = {'Authorization': 'Bearer ' + token}
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(url, proxies=proxyDict, json=data, headers=headers)
    if r.status_code == 200:
        id_esr = r.json()['institution']['id']
        logging.info('%s: new institution created in ESR with id %s',
                     numero_uai, id_esr)
        count += 1
        create_numero_uai(numero_uai, id_esr, headers, code_categories)
        create_address(patronyme_uai, adresse_uai, boite_postale_uai,
                       code_postal_uai, localite_acheminement_uai,
                       numero_telephone_uai, id_esr, headers)
        create_ministere_tutelle(ministere_tutelle, id_esr, headers)
        create_public_prive(secteur_public_prive, id_esr, headers)
        create_categorie_juridique(categorie_juridique, id_esr, headers)
        if site_web:
            create_website(site_web, id_esr, headers, link_categories)
        if numero_siren_siret_uai:
            create_siret(numero_siren_siret_uai, id_esr, headers,
                         code_categories)
    else:
        logging.error('%s: unable to create institution in dataESR',
                      numero_uai)
    return count


def create_numero_uai(numero_uai, id_esr, headers, code_categories):
    code_category_id = find_category_id(code_categories, 'numero_uai')
    data = {"code":
            {"content": numero_uai, "code_category_id": code_category_id}}
    url = os.getenv('INSTITUTION_URL')+'institutions/' + str(id_esr) + '/codes'
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(url, json=data, headers=headers, proxies=proxyDict)
    if r.status_code == 200:
        logging.debug('%s: UAI created', id_esr)
    else:
        logging.error('%s: UAI not created', id_esr)


def create_address(patronyme_uai, adresse_uai, boite_postale_uai,
                   code_postal_uai, localite_acheminement_uai,
                   numero_telephone_uai, id_esr, headers):
    data = {"address":
            {"business_name": patronyme_uai,
             "address_1": adresse_uai,
             "address_2": boite_postale_uai,
             "zip_code": code_postal_uai,
             "city": localite_acheminement_uai,
             "country": "France",
             "phone": numero_telephone_uai}}
    url = (os.getenv('INSTITUTION_URL')+'institutions/' + str(id_esr) +
           '/addresses')
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(url, json=data, headers=headers, proxies=proxyDict)
    if r.status_code == 200:
        logging.debug('%s: address created', id_esr)
    else:
        logging.error('%s: address not created', id_esr)


def create_ministere_tutelle(ministere_tutelle, id_esr, headers):
    data = {"institution_tagging": {"date_start": '2000-01-01'}}
    url = (os.getenv('INSTITUTION_URL') + 'institutions/' + str(id_esr) +
           '/tags/' + str(ministere_dict[ministere_tutelle]))

    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(url, json=data, headers=headers, proxies=proxyDict)
    if r.status_code == 200:
        logging.debug('%s: ministere_tutelle created', id_esr)
    else:
        logging.error('%s: ministere_tutelle not created', id_esr)


def create_public_prive(secteur_public_prive, id_esr, headers):
    data = {"institution_tagging": {"date_start": '2000-01-01'}}
    url = (os.getenv('INSTITUTION_URL') + 'institutions/' + str(id_esr) +
           '/tags/' + str(public_prive_dict[secteur_public_prive]))
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(url, json=data, headers=headers, proxies=proxyDict)
    if r.status_code == 200:
        logging.debug('%s: secteur_public_prive created', id_esr)
    else:
        logging.error('%s: secteur_public_prive not created', id_esr)


def create_categorie_juridique(categorie_juridique, id_esr, headers):
    data = {"institution_tagging": {"date_start": '2000-01-01'}}
    url = (os.getenv('INSTITUTION_URL') + 'institutions/' + str(id_esr) +
           '/tags/' + str(cat_juridiques_dict[categorie_juridique]))
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(url, json=data, headers=headers, proxies=proxyDict)
    if r.status_code == 200:
        logging.debug('%s: categorie_juridique created', id_esr)
    else:
        logging.error('%s: categorie_juridique not created', id_esr)


def create_website(site_web, id_esr, headers, link_categories):
    link_category_id = find_category_id(link_categories, 'site_web')
    data = {"link":
            {"content": site_web, 'link_category_id': link_category_id}}
    url = os.getenv('INSTITUTION_URL')+'institutions/' + str(id_esr) + '/links'
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(url, json=data, headers=headers, proxies=proxyDict)
    if r.status_code == 200:
        logging.debug('%s: site_web created', id_esr)
    else:
        logging.error('%s: site_web not created', id_esr)


def create_siret(numero_siren_siret_uai, id_esr, headers, code_categories):
    code_category_id = find_category_id(
        code_categories, 'numero_siren_siret_uai')
    data = {"code":
            {"content": numero_siren_siret_uai,
             "code_category_id": code_category_id}}
    url = os.getenv('INSTITUTION_URL')+'institutions/' + str(id_esr) + '/codes'
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(url, json=data, headers=headers, proxies=proxyDict)
    if r.status_code == 200:
        logging.debug('%s: numero_siren_siret_uai created', id_esr)
    else:
        logging.error('%s: numero_siren_siret_uai not created', id_esr)
