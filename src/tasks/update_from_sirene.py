
import logging
import os
import requests
from repositories import SireneSnapshotRepository
from .authenticate import authenticate
from .check_conflict import (check_for_all_conflict, check_for_all_conflict_with_snapshot)
from .get_data import get_institution_from_esr
from models import SireneInstitution
from datetime import date


def update_from_sirene():
    logging.info('#### START update from sirene #####')
    esr_token = authenticate()
    sirene_token = os.getenv('SIRENE_TOKEN')
    logging.info('TOKEN')
    logging.info(sirene_token)

    institutions = SireneInstitution.query.all()
    for institution in institutions:
        logging.info('\n')
        logging.info(institution.siret)

        url = os.getenv('SIRENE_ETABLISSEMENT_URL')+str(institution.siret)+'?token='+sirene_token+'&context=APS&recipient=123&object=abc'
        logging.info(url)
        proxyDict = {"http": os.getenv('HTTP_PROXY')}
        r = requests.get(url, proxies=proxyDict)
        if r.status_code == 200:
            # id_esr = r.json()['institution']['id']
            logging.info('youpi : Etablissement caught from SIRENE api')
            etablissement_json = r.json()['etablissement']
            logging.info(etablissement_json)
            update_date = date.fromtimestamp(etablissement_json['date_mise_a_jour'])
            if update_date > institution.date_maj.date():

                logging.info("UPDATE !! We need to create a snapshot")
                # CREATE A SNAPSHOT(r.json())

                # get snapshot if existing
                snapshot = SireneSnapshotRepository.get(siret=etablissement_json['siret'])
                logging.info('Snapshot : %s', snapshot)

                # 2. Try to get esr institution
                esr_institution = get_institution_from_esr(source_id=etablissement_json['siret'], token=esr_token)
                if esr_institution is not None:
                    logging.info('institution found in dataESR')
                    logging.info(esr_institution)
                    esr_institution = esr_institution['institution']

                # If existing snapshot
                if esr_institution and snapshot is None:
                    logging.info('pas de snapshot')
                    compare_esr_without_snapshot(siret=etablissement_json['siret'],
                                                 business_name=etablissement_json['adresse']['l1'],
                                                 address_1=etablissement_json['adresse']['l4'],
                                                 address_2=etablissement_json['adresse']['l5'],
                                                 zip_code=etablissement_json['adresse']['code_postal'],
                                                 city=etablissement_json['adresse']['localite'],
                                                 country='France',
                                                 city_code=etablissement_json['adresse']['localite'],
                                                 naf=etablissement_json['naf'],
                                                 date_ouverture=date.fromtimestamp(etablissement_json['date_creation_etablissement']),
                                                 tranche_effectif=etablissement_json['tranche_effectif_salarie_etablissement']['intitule'],
                                                 esr_institution=esr_institution)

                elif esr_institution:
                    logging.info('Le snap existe, il faut le mettre à jour')
                    compare_esr_with_snapshot(siret=etablissement_json['siret'],
                                              business_name=etablissement_json['adresse']['l1'],
                                              address_1=etablissement_json['adresse']['l4'],
                                              address_2=etablissement_json['adresse']['l5'],
                                              zip_code=etablissement_json['adresse']['code_postal'],
                                              city=etablissement_json['adresse']['localite'],
                                              country='France',
                                              city_code=etablissement_json['adresse']['localite'],
                                              naf=etablissement_json['naf'],
                                              date_ouverture=date.fromtimestamp(etablissement_json['date_creation_etablissement']),
                                              tranche_effectif=etablissement_json['tranche_effectif_salarie_etablissement']['intitule'],
                                              snapshot=snapshot,
                                              esr_institution=esr_institution)

                else:
                    logging.info('No institution found')

        else:
            logging.info(r.status_code)


def compare_esr_without_snapshot(
        siret, business_name, address_1, address_2, zip_code, city, country, city_code, naf, date_ouverture,
        tranche_effectif, esr_institution):
    logging.info('in compare without snapshot')
    # 1. create missing snapshot
    SireneSnapshotRepository.create(
        SireneSnapshotRepository(), siret, business_name, address_1, address_2, zip_code, city, country, city_code,
        naf, date_ouverture, tranche_effectif)
    logging.info('%s: snapshot created', siret)

    # if institution exists in dataESR, check for conflicts
    check_for_all_conflict(
        siret, business_name, address_1, address_2, zip_code, city, country, city_code, naf, date_ouverture,
        tranche_effectif, esr_institution)


def compare_esr_with_snapshot(
        siret, business_name, address_1, address_2, zip_code, city, country, city_code, naf, date_ouverture,
        tranche_effectif, snapshot, esr_institution):

    check_for_all_conflict_with_snapshot(
        siret, business_name, address_1, address_2, zip_code, city, country, city_code, naf, date_ouverture,
        tranche_effectif, esr_institution, snapshot)

    # Update snpashot with new values
    SireneSnapshotRepository.update(
        SireneSnapshotRepository(), siret, business_name, address_1, address_2, zip_code,
        city, country, city_code, naf, date_ouverture, tranche_effectif)
