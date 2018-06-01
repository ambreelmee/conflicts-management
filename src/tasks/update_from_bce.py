
import logging
import psycopg2
import os
from repositories import InstitutionRepository, InstitutionSnapshotRepository
from .authenticate import authenticate
from .conflict import check_for_all_conflict, check_for_conflict
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

conn = psycopg2.connect(**params)


def compare_esr_without_snapshot(
        numero_uai, sigle_uai, patronyme_uai, date_ouverture, date_fermeture,
        numero_siren_siret_uai, adresse_uai, boite_postale_uai,
        code_postal_uai, localite_acheminement_uai, numero_telephone_uai,
        secteur_public_prive, ministere_tutelle, categorie_juridique,
        site_web, token, link_categories, code_categories, count):

    # 1. create missing snapshot
    InstitutionSnapshotRepository.create(
        numero_uai=numero_uai, sigle_uai=sigle_uai,
        patronyme_uai=patronyme_uai, date_ouverture=date_ouverture,
        date_fermeture=date_fermeture,
        numero_siren_siret_uai=numero_siren_siret_uai,
        adresse_uai=adresse_uai, boite_postale_uai=boite_postale_uai,
        code_postal_uai=code_postal_uai,
        localite_acheminement_uai=localite_acheminement_uai,
        numero_telephone_uai=numero_telephone_uai,
        secteur_public_prive=secteur_public_prive,
        ministere_tutelle=ministere_tutelle,
        categorie_juridique=categorie_juridique, site_web=site_web)
    logging.debug('%s: snapshot created', numero_uai)

    # 2. Try to get esr institution
    esr_institution = get_institution_from_esr(
        uai_number=numero_uai)
    if not esr_institution:
        logging.debug('instution not found in dataESR')

        # if no institution is found, create one
        count_new_institution_dataESR = create_esr_institution(
            token=token, numero_uai=numero_uai, sigle_uai=sigle_uai,
            patronyme_uai=patronyme_uai, date_ouverture=date_ouverture,
            date_fermeture=date_fermeture,
            numero_siren_siret_uai=numero_siren_siret_uai,
            adresse_uai=adresse_uai, boite_postale_uai=boite_postale_uai,
            code_postal_uai=code_postal_uai,
            localite_acheminement_uai=localite_acheminement_uai,
            numero_telephone_uai=numero_telephone_uai,
            secteur_public_prive=secteur_public_prive,
            ministere_tutelle=ministere_tutelle,
            categorie_juridique=categorie_juridique, site_web=site_web,
            link_categories=link_categories,
            code_categories=code_categories,
            count=count)

    # if institution exists in dataESR, check for conflicts
    if esr_institution:
        logging.debug('institution found in dataESR')
        esr_institution = esr_institution['institution']
        check_for_all_conflict(
            numero_uai=numero_uai, sigle_uai=sigle_uai,
            patronyme_uai=patronyme_uai, date_ouverture=date_ouverture,
            date_fermeture=date_fermeture,
            numero_siren_siret_uai=numero_siren_siret_uai,
            adresse_uai=adresse_uai, boite_postale_uai=boite_postale_uai,
            code_postal_uai=code_postal_uai,
            localite_acheminement_uai=localite_acheminement_uai,
            numero_telephone_uai=numero_telephone_uai,
            secteur_public_prive=secteur_public_prive,
            ministere_tutelle=ministere_tutelle,
            categorie_juridique=categorie_juridique, site_web=site_web,
            esr_institution=esr_institution)
    return count_new_institution_dataESR


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
    token = authenticate()['access_token']

    # in order to create or update some categories, we need to get the
    # connection between categories names stored in database connection
    # and their ids
    link_categories = get_link_categories(token)
    code_categories = get_code_categories(token)

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
                site_web FROM bce_uai""")
            rows = curs.fetchall()
            logging.info('start processing data')
            for row in rows:
                count_new_institution_bce = 0
                count_new_institution_dataESR = 0
                # get the saved institution for a given uai number
                # institution will be None if it doesn't exist in our database
                institution = InstitutionRepository.get(uai_number=row[0])
                # case of new institution in bce
                if not institution:
                    logging.info('%s: institution not in database', row[0])
                    # default value that can be later overriden by user
                    is_institution = row[1] in list_nature_uai

                    # save the institution
                    InstitutionRepository.create(
                        uai_number=row[0], is_institution=is_institution)
                    logging.info('%s: institution created with %s',
                                 row[0], is_institution)
                    count_new_institution_bce += 1
                    # create new snapshot if institution is in ESR scope
                    if is_institution:
                        compare_esr_without_snapshot(
                            token=token, numero_uai=row[0], sigle_uai=row[2],
                            patronyme_uai=row[3], date_ouverture=row[4],
                            date_fermeture=row[5],
                            numero_siren_siret_uai=row[6],
                            adresse_uai=row[7], boite_postale_uai=row[8],
                            code_postal_uai=row[9],
                            localite_acheminement_uai=row[10],
                            numero_telephone_uai=row[11],
                            secteur_public_prive=row[12],
                            ministere_tutelle=row[13],
                            categorie_juridique=row[14], site_web=row[15],
                            link_categories=link_categories,
                            code_categories=code_categories,
                            count=count_new_institution_dataESR)

                # case of already existing institution
                else:
                    # check if insitution is in ESR scope
                    if institution.is_institution:

                        # get snapshot
                        snapshot = InstitutionSnapshotRepository.get(
                            numero_uai=row[0])

                        # case of snapshot  found in database
                        # (this case should not happen)
                        if not snapshot:
                            logging.debug('no snapshot found')
                            compare_esr_without_snapshot(
                                token=token, numero_uai=row[0],
                                sigle_uai=row[2], patronyme_uai=row[3],
                                date_ouverture=row[4], date_fermeture=row[5],
                                numero_siren_siret_uai=row[6],
                                adresse_uai=row[7], boite_postale_uai=row[8],
                                code_postal_uai=row[9],
                                localite_acheminement_uai=row[10],
                                numero_telephone_uai=row[11],
                                secteur_public_prive=row[12],
                                ministere_tutelle=row[13],
                                categorie_juridique=row[14], site_web=row[15],
                                link_categories=link_categories,
                                code_categories=code_categories,
                                count=count_new_institution_dataESR)

                        # if a snapshot is found
                        else:
                            # get the ESR institution for a given uai number
                            esr_institution = get_institution_from_esr(
                                uai_number=row[0])
                            if not esr_institution:
                                count_new_institution_dataESR = create_esr_institution(
                                    token=token, numero_uai=row[0],
                                    sigle_uai=row[2], patronyme_uai=row[3],
                                    date_ouverture=row[4], date_fermeture=row[5],
                                    numero_siren_siret_uai=row[6],
                                    adresse_uai=row[7], boite_postale_uai=row[8],
                                    code_postal_uai=row[9],
                                    localite_acheminement_uai=row[10],
                                    numero_telephone_uai=row[11],
                                    secteur_public_prive=row[12],
                                    ministere_tutelle=row[13],
                                    categorie_juridique=row[14], site_web=row[15],
                                    link_categories=link_categories,
                                    code_categories=code_categories,
                                    count=count_new_institution_dataESR)
                            # institution found in dataESR
                            else:
                                # for each bce field of the bce snapshot
                                # checks if value has been updated in bce
                                # and check for conflict if it's the case
                                if snapshot.sigle_uai != row[2]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='sigle_uai',
                                        bce_value=row[2],
                                        esr_institution=esr_institution)

                                if snapshot.patronyme_uai != row[3]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='patronyme_uai',
                                        bce_value=row[3],
                                        esr_institution=esr_institution)

                                if snapshot.date_ouverture != row[4]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='date_ouverture',
                                        bce_value=row[4],
                                        esr_institution=esr_institution)

                                if snapshot.date_fermeture != row[5]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='date_fermeture',
                                        bce_value=row[5],
                                        esr_institution=esr_institution)

                                if snapshot.numero_siren_siret_uai != row[6]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='numero_siren_siret_uai',
                                        bce_value=row[6],
                                        esr_institution=esr_institution)

                                if snapshot.adresse_uai != row[7]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='adresse_uai',
                                        bce_value=row[7],
                                        esr_institution=esr_institution)

                                if snapshot.boite_postale_uai != row[8]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='boite_postale_uai',
                                        bce_value=row[8],
                                        esr_institution=esr_institution)

                                if snapshot.code_postal_uai != row[9]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='code_postal_uai',
                                        bce_value=row[9],
                                        esr_institution=esr_institution)

                                if (snapshot.localite_acheminement_uai !=
                                        row[10]):
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='localite_acheminement_uai',
                                        bce_value=row[10],
                                        esr_institution=esr_institution)

                                if snapshot.numero_telephone_uai != row[11]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='numero_telephone_uai',
                                        bce_value=row[11],
                                        esr_institution=esr_institution)

                                if snapshot.secteur_public_prive != row[12]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='secteur_public_prive',
                                        bce_value=row[12],
                                        esr_institution=esr_institution)

                                if snapshot.ministere_tutelle != row[13]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='ministere_tutelle',
                                        bce_value=row[13],
                                        esr_institution=esr_institution)

                                if snapshot.categorie_juridique != row[14]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='categorie_juridique',
                                        bce_value=row[14],
                                        esr_institution=esr_institution)

                                if snapshot.site_web != row[15]:
                                    check_for_conflict(
                                        uai_number=row[0],
                                        field_name='site_web',
                                        bce_value=row[15],
                                        esr_institution=esr_institution)

                            # Update snpashot with new values
                            InstitutionSnapshotRepository.update(
                                InstitutionSnapshotRepository(),
                                numero_uai=row[0],
                                sigle_uai=row[2],
                                patronyme_uai=row[3],
                                date_ouverture=row[4],
                                date_fermeture=row[5],
                                numero_siren_siret_uai=row[6],
                                adresse_uai=row[7],
                                boite_postale_uai=row[8],
                                code_postal_uai=row[9],
                                localite_acheminement_uai=row[10],
                                numero_telephone_uai=row[11],
                                secteur_public_prive=row[12],
                                ministere_tutelle=row[13],
                                categorie_juridique=row[14],
                                site_web=row[15])
    logging.info('update comleted')
    logging.info('%s: new institutions from bce', count_new_institution_bce)
    logging.info('%s: new institutions created in dataESR',
                 count_new_institution_dataESR)
    return
