from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import psycopg2
import requests
import os
import config
from models import db
from repositories import (
    InstitutionRepository, InstitutionSnapshotRepository,
    ConflictRepository, DatabaseConnectionRepository)

server = Flask(__name__)
server.debug = config.DEBUG
server.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
db.init_app(server)

migrate = Migrate(server, db)
manager = Manager(server)
manager.add_command('db', MigrateCommand)

params = {
  'dbname': os.getenv('REMOTE_DB_NAME'),
  'user': os.getenv('REMOTE_DB_USER'),
  'password': os.getenv('REMOTE_DB_PASSWORD'),
  'host': os.getenv('REMOTE_DB_HOST'),
  'port': os.getenv('REMOTE_DB_PORT')
}

conn = psycopg2.connect(**params)


def get_institution_from_esr(uai_number):
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    r = requests.post(
        os.getenv('INSTITUTION_URL')+'codes/search?q=' + uai_number,
        proxies=proxyDict)
    if r.status_code == 200:
        print (r.json())
        if r.json()['message'] == 'No institution':
            return None
        return r.json()
    print (uai_number, ' institution not found in dataESR')
    return None


def get_esr_value(bce_field, esr_institution):
    connections = DatabaseConnectionRepository.get(bce_field=bce_field)
    bloc = esr_institution[connections.bloc] if connections['bloc'] else esr_institution

    if not connections.criterion_key:
        return bloc[connections.value_key]
    return next((item[connections.value_key] for item in bloc
                if (item[connections.criterion_key] ==
                    item[connections.criterion_value])), None)




@manager.command
def saveInstitutionInformation():
    """ for each value of bce_uai table in bce
    set up is_institution value in Institution table
    and save further information about each institution
    if it is in ESR scode"""

    # list of codes to filter bce with only institutions in ESR scope
    list_nature_uai = [
        '400', '410', '420', '445', '455', '470', '480', '490', '500', '502',
        '503', '505', '506', '507', '523', '524', '547', '550', '551', '553',
        '554', '560', '562', '580', '848']
    public_prive_dict = {'PU': 35, 'PR': 36}
    ministere_dict = {'38': 6, '06': 7, '01': 8, '02': 9, '04': 10, '05': 11,
                      '08': 12, '09': 13, '12': 14, '16': 15, '18': 16,
                      '22': 17, '23': 18, '25': 19, '32': 20, '35': 21,
                      '37': 22, '60': 23, '80': 24, '00': 25, '21': 26,
                      '28': 27, '30': 28, '36': 29, '**': 30, '03': 31,
                      '10': 32, '20': 33, '33': 34}
    cat_juridiques_dict = {'254': 94, '264': 95, '311': 96, '101': 97,
                           '111': 98, '121': 99, '131': 100, '141': 101,
                           '200': 102, '210': 103, '220': 104, '230': 105,
                           '240': 106, '250': 107, '260': 108, '270': 109,
                           '280': 110, '300': 111, '310': 112, '321': 113,
                           '331': 114, '255': 115, '201': 116, '281': 117,
                           '282': 118, '283': 119, '284': 120, '285': 121,
                           '500': 122, '999': 123, '341': 124, '151': 125,
                           '251': 126, '252': 127, '253': 128, '256': 129,
                           '257': 130, '258': 131, '259': 132, '320': 133,
                           '350': 134, '351': 135, '221': 136, '261': 137,
                           '286': 138, '!!!': ''}
    with conn:
        with conn.cursor() as curs:
            # select all rows in bce uai
            curs.execute(
                """ SELECT
                    numero_uai,
                    nature_uai,
                    sigle_uai,
                    patronyme_uai,
                    date_ouverture,
                    date_fermeture,
                    numero_siren_siret_uai,
                    adresse_uai,
                    boite_postale_uai,
                    code_postal_uai,
                    localite_acheminement_uai,
                    numero_telephone_uai,
                    secteur_public_prive,
                    ministere_tutelle,
                    categorie_juridique,
                    site_web
                FROM bce_uai""")
            rows = curs.fetchall()
            for row in rows:
                # get the saved institution for a given uai number
                institution = InstitutionRepository.get(uai_number=row[0])

                # case of new institution in bce
                if not institution:
                    # default value that can be later overriden by user
                    is_institution = row[1] in list_nature_uai

                    # save the institution
                    InstitutionRepository.create(
                        uai_number=row[0], is_institution=is_institution)
                    print(row[0], ': institution created with ', is_institution)
                    # save all fields if insitution is in ESR scope
                    if is_institution:
                        InstitutionSnapshotRepository.create(
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
                        print(row[0], ': snapshot created')

                # case of already existing institution
                if institution:

                    # check if insitution is in ESR scope
                    if institution.is_institution:

                        # get the ESR institution for a given uai number
                        esr_institution = get_institution_from_esr(
                            uai_number=row[0])

                        # create one if it does not exists
                        if not esr_institution:
                            create_esr_institution(numero_uai=row[0],
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
                        if esr_institution:
                        esr_institution = esr_institution.institution
                        # get the snapshot value previously saved
                        snapshot = InstitutionSnapshotRepository.get(
                            uai_number=row[0])

                        # for each bce field of the bce snapshot
                        # checks if value has been updated in bce
                        # then compares with the current value in dataESR
                        # and creates a new conflict if different
                        # save the new value of snapshot anyway

                        if snapshot.sigle_uai != row[2]:
                            esr_value = get_esr_value(
                                bce_field='sigle_uai',
                                esr_institution=esr_institution)
                            if esr_value != row[2]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='sigle_uai',
                                    current_value=esr_value,
                                    new_value=row[2],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field sigle_uai')

                        if snapshot.patronyme_uai != row[3]:
                            esr_value = get_esr_value(
                                bce_field='patronyme_uai',
                                esr_institution=esr_institution)
                            if esr_value != row[3]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='patronyme_uai',
                                    current_value=esr_value,
                                    new_value=row[3],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field patronyme_uai')

                        if snapshot.date_ouverture != row[4]:
                            esr_value = get_esr_value(
                                bce_field='date_ouverture',
                                esr_institution=esr_institution)
                            if esr_value != row[4]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='date_ouverture',
                                    current_value=esr_value,
                                    new_value=row[4],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field date_ouverture')

                        if snapshot.date_fermeture != row[5]:
                            esr_value = get_esr_value(
                                bce_field='date_fermeture',
                                esr_institution=esr_institution)
                            if esr_value != row[5]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='date_fermeture',
                                    current_value=esr_value,
                                    new_value=row[5],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field date_fermeture')

                        if snapshot.numero_siren_siret_uai != row[6]:
                            esr_value = get_esr_value(
                                bce_field='numero_siren_siret_uai',
                                esr_institution=esr_institution)
                            if esr_value != row[6]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='numero_siren_siret_uai',
                                    current_value=esr_value,
                                    new_value=row[6],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field numero_siren_siret_uai')

                        if snapshot.adresse_uai != row[7]:
                            esr_value = get_esr_value(
                                bce_field='adresse_uai',
                                esr_institution=esr_institution)
                            if esr_value != row[7]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='adresse_uai',
                                    current_value=esr_value,
                                    new_value=row[7],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field adresse_uai')

                        if snapshot.boite_postale_uai != row[8]:
                            esr_value = get_esr_value(
                                bce_field='boite_postale_uai',
                                esr_institution=esr_institution)
                            if esr_value != row[8]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='boite_postale_uai',
                                    current_value=esr_value,
                                    new_value=row[8],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field boite_postale_uai')

                        if snapshot.code_postal_uai != row[9]:
                            esr_value = get_esr_value(
                                bce_field='code_postal_uai',
                                esr_institution=esr_institution)
                            if esr_value != row[9]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='code_postal_uai',
                                    current_value=esr_value,
                                    new_value=row[9],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field code_postal_uai')

                        if snapshot.localite_acheminement_uai != row[10]:
                            esr_value = get_esr_value(
                                bce_field='localite_acheminement_uai',
                                esr_institution=esr_institution)
                            if esr_value != row[10]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='localite_acheminement_uai',
                                    current_value=esr_value,
                                    new_value=row[10],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field localite_acheminement_uai')

                        if snapshot.numero_telephone_uai != row[11]:
                            esr_value = get_esr_value(
                                bce_field='numero_telephone_uai',
                                esr_institution=esr_institution)
                            if esr_value != row[11]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='numero_telephone_uai',
                                    current_value=esr_value,
                                    new_value=row[11],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field numero_telephone_uai')

                        if snapshot.secteur_public_prive != row[12]:
                            esr_value = get_esr_value(
                                bce_field='secteur_public_prive',
                                esr_institution=esr_institution)
                            if esr_value != public_prive_dict[row[12]]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='secteur_public_prive',
                                    current_value=esr_value,
                                    new_value=public_prive_dict[row[12]],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field secteur_public_prive')

                        if snapshot.ministere_tutelle != row[13]:
                            esr_value = get_esr_value(
                                bce_field='ministere_tutelle',
                                esr_institution=esr_institution)
                            if esr_value != ministere_dict[row[13]]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='ministere_tutelle',
                                    current_value=esr_value,
                                    new_value=ministere_dict[row[13]],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field ministere_tutelle')

                        if snapshot.categorie_juridique != row[14]:
                            esr_value = get_esr_value(
                                bce_field='categorie_juridique',
                                esr_institution=esr_institution)
                            if esr_value != cat_juridiques_dict[row[14]]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='categorie_juridique',
                                    current_value=esr_value,
                                    new_value=cat_juridiques_dict[row[14]],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field categorie_juridique')

                        if snapshot.site_web != row[15]:
                            esr_value = get_esr_value(
                                bce_field='site_web',
                                esr_institution=esr_institution)
                            if esr_value != row[15]:
                                ConflictRepository.create(
                                    uai_number=row[0],
                                    field_name='site_web',
                                    current_value=esr_value,
                                    new_value=row[15],
                                    active=True,
                                    id_esr=esr_institution.id)
                                print(row[0], ': conflict with field site_web')


                            # Update snpashot with new values
                            snapshot.update(
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
                            print(row[0], ': snapshot updated')


if __name__ == '__main__':
    manager.run()
