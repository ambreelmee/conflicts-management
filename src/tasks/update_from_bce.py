import logging
import psycopg2
import os
from repositories import BceInstitutionRepository, BceSnapshotRepository
from .authenticate import authenticate
from .check_conflict import (
    check_for_all_bce_conflict, check_for_all_bce_conflict_with_snapshot)
from .create_esr_institution import create_esr_institution
from .get_data import (
    get_code_categories, get_link_categories, get_institution_from_esr)

params = {
  'dbname': os.getenv('REMOTE_DB_NAME'),
  'user': os.getenv('REMOTE_DB_USER'),
  'password': os.getenv('REMOTE_DB_PASSWORD'),
  'host': os.getenv('REMOTE_DB_HOST'),
  'port': os.getenv('REMOTE_DB_PORT')
}


def compare_esr_without_snapshot(
        uai, sigle, patronyme, date_ouverture, date_fermeture,
        numero_siren_siret, adresse, boite_postale,
        code_postal, localite_acheminement, numero_telephone,
        secteur_public_prive, ministere_tutelle, categorie_juridique,
        site_web, commune, token, link_categories, code_categories,
        count):

    # 1. create missing snapshot
    BceSnapshotRepository.create(
        uai, sigle, patronyme, date_ouverture, date_fermeture,
        numero_siren_siret, adresse, boite_postale,
        code_postal, localite_acheminement, numero_telephone,
        secteur_public_prive, ministere_tutelle, categorie_juridique,
        site_web, commune)
    logging.debug('%s: snapshot created', uai)

    # 2. Try to get esr institution
    esr_institution = get_institution_from_esr(source_id=uai, token=token)
    if not esr_institution:
        logging.debug('instution not found in dataESR')

        # if no institution is found, create one
        count = create_esr_institution(
            token, uai, sigle, patronyme, date_ouverture,
            date_fermeture, numero_siren_siret, adresse,
            boite_postale, code_postal, localite_acheminement,
            numero_telephone, secteur_public_prive, ministere_tutelle,
            categorie_juridique, site_web, commune, link_categories,
            code_categories, count)

    # if institution exists in dataESR, check for conflicts
    else:
        logging.debug('institution found in dataESR')
        esr_institution = esr_institution['institution']
        check_for_all_bce_conflict(
            uai, sigle, patronyme, date_ouverture,
            date_fermeture, numero_siren_siret, adresse,
            boite_postale, code_postal, localite_acheminement,
            numero_telephone, secteur_public_prive, ministere_tutelle,
            categorie_juridique, site_web, commune, esr_institution)
    return count


def compare_esr_with_snapshot(
        uai, sigle, patronyme, date_ouverture,
        date_fermeture, numero_siren_siret, adresse, boite_postale,
        code_postal, localite_acheminement, numero_telephone,
        secteur_public_prive, ministere_tutelle, categorie_juridique,
        site_web, commune, token, link_categories, code_categories,
        count, snapshot):

    # get the ESR institution for a given uai number
    esr_institution = get_institution_from_esr(uai, token)

    if not esr_institution:
        count = create_esr_institution(
            token, uai, sigle, patronyme, date_ouverture,
            date_fermeture, numero_siren_siret, adresse,
            boite_postale, code_postal, localite_acheminement,
            numero_telephone, secteur_public_prive, ministere_tutelle,
            categorie_juridique, site_web, commune, link_categories,
            code_categories, count)
    # institution found in dataESR
    else:
        esr_institution = esr_institution['institution']
        check_for_all_bce_conflict_with_snapshot(
            uai, sigle, patronyme, date_ouverture,
            date_fermeture, numero_siren_siret, adresse,
            boite_postale, code_postal, localite_acheminement,
            numero_telephone, secteur_public_prive, ministere_tutelle,
            categorie_juridique, site_web, commune, esr_institution, snapshot)

    # Update snpashot with new values
    BceSnapshotRepository.update(
        BceSnapshotRepository(), uai, sigle,
        patronyme, date_ouverture, date_fermeture,
        numero_siren_siret, adresse, boite_postale,
        code_postal, localite_acheminement, numero_telephone,
        secteur_public_prive, ministere_tutelle, categorie_juridique,
        site_web, commune)
    return count


def update_from_bce():
    """ for each value of bce_uai table in bce
    set up is_institution value in Institution table
    and save further information about each institution
    if it is in ESR scode"""

    # list of codes to filter bce with only institutions in ESR scope
    logging.info('start')
    list_nature_uai = [
        '400', '410', '420', '445', '455', '470', '480', '490', '500', '502',
        '503', '505', '506', '507', '523', '524', '547', '550', '551', '553',
        '554', '560', '562', '580', '848']

    # in order to create any institution, we need to be authenticated
    token = authenticate()

    # in order to create or update some categories, we need to get the
    # connection between categories names stored in database connection
    # and their ids
    link_categories = get_link_categories(token)
    code_categories = get_code_categories(token)
    count_new_institution_bce = 0
    count_new_institution_dataESR = 0
    conn = psycopg2.connect(**params)

    with conn:
        with conn.cursor() as curs:
            # select all rows in bce uai
            logging.debug('fetching data from bce...')
            curs.execute(
                """ SELECT numero_uai, nature_uai, sigle_uai, patronyme_uai,
                date_ouverture, date_fermeture, numero_siren_siret_uai,
                adresse_uai, boite_postale_uai, code_postal_uai,
                localite_acheminement_uai, numero_telephone_uai,
                secteur_public_prive, ministere_tutelle, categorie_juridique,
                site_web, commune FROM bce_uai""")
            logging.info('start processing data')
            logging.info('%s', curs)
            for row in curs:
                # get the saved institution for a given uai number
                # institution will be None if it doesn't exist in our database
                institution = BceInstitutionRepository.get(uai=row[0])

                # get snapshot if existing
                snapshot = BceSnapshotRepository.get(uai=row[0])

                # case of new institution in bce
                if not (institution or snapshot):
                    logging.info('%s: institution not in database', row[0])
                    # default value that can be later overriden by user
                    is_institution = row[1] in list_nature_uai

                    # save the institution
                    BceInstitutionRepository.create(
                        uai=row[0], is_institution=is_institution)
                    logging.info('%s: institution created with %s', row[0], is_institution)
                    count_new_institution_bce += 1

                    # create new snapshot if institution is in ESR scope
                    if is_institution:
                        count_new_institution_dataESR = (
                            compare_esr_without_snapshot(
                                token=token, uai=row[0],
                                sigle=row[2], patronyme=row[3],
                                date_ouverture=row[4], date_fermeture=row[5],
                                numero_siren_siret=row[6],
                                adresse=row[7], boite_postale=row[8],
                                code_postal=row[9],
                                localite_acheminement=row[10],
                                numero_telephone=row[11],
                                secteur_public_prive=row[12],
                                ministere_tutelle=row[13],
                                categorie_juridique=row[14], site_web=row[15],
                                commune=row[16],
                                link_categories=link_categories,
                                code_categories=code_categories,
                                count=count_new_institution_dataESR))

                # case of already existing institution in dataESR scope
                # but no snapshot found (should not happen usually)
                elif institution.is_institution and not snapshot:
                    logging.debug('no snapshot found')
                    count_new_institution_dataESR = (
                        compare_esr_without_snapshot(
                            token=token, uai=row[0], sigle=row[2],
                            patronyme=row[3], date_ouverture=row[4],
                            date_fermeture=row[5],
                            numero_siren_siret=row[6], adresse=row[7],
                            boite_postale=row[8], code_postal=row[9],
                            localite_acheminement=row[10],
                            numero_telephone=row[11],
                            secteur_public_prive=row[12],
                            ministere_tutelle=row[13],
                            categorie_juridique=row[14], site_web=row[15],
                            commune=row[16],
                            link_categories=link_categories,
                            code_categories=code_categories,
                            count=count_new_institution_dataESR))

                # if a snapshot is found
                elif institution.is_institution and snapshot:
                    count_new_institution_dataESR = (
                        compare_esr_with_snapshot(
                            token=token, uai=row[0], sigle=row[2],
                            patronyme=row[3], date_ouverture=row[4],
                            date_fermeture=row[5],
                            numero_siren_siret=row[6], adresse=row[7],
                            boite_postale=row[8], code_postal=row[9],
                            localite_acheminement=row[10],
                            numero_telephone=row[11],
                            secteur_public_prive=row[12],
                            ministere_tutelle=row[13],
                            categorie_juridique=row[14], site_web=row[15],
                            commune=row[16], link_categories=link_categories,
                            code_categories=code_categories,
                            count=count_new_institution_dataESR,
                            snapshot=snapshot))
    logging.info('update comleted')
    logging.info('%s: new institutions from bce', count_new_institution_bce)
    logging.info('%s: new institutions created in dataESR',
                 count_new_institution_dataESR)
    return ({'bce_count': count_new_institution_bce,
             'esr_count': count_new_institution_dataESR})
