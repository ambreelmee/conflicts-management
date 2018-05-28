from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import psycopg2

import os
import config
from models import db
from repositories import InstitutionRepository
from repositories import InstitutionSnapshotRepository

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
                    site_web,
                    coordonnee_x,
                    coordonnee_y
                FROM bce_uai""")
            rows = curs.fetchall()
            for row in rows:
                isInstitution = row[1] in list_nature_uai  # check if in scope
                InstitutionRepository.create(
                            uai_number=row[0], is_institution=isInstitution)
                print (row[0], isInstitution, ' successfully created')
                if isInstitution:
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
                        site_web=row[15],
                        coordonnee_x=row[16],
                        coordonnee_y=row[17])
                    print (row[0], isInstitution,
                           'additionnal information collected')


if __name__ == '__main__':
    manager.run()
