import unittest

from server import server
from models.abc import db
from repositories import InstitutionSnapshotRepository


class TestInstitutionSnapshot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create(self):
        institution = InstitutionSnapshotRepository.create(
             numero_uai='0802145Y',
             sigle_uai='TEST',
             patronyme_uai='TEST',
             date_ouverture='2012-02-03',
             date_fermeture='2012-02-04',
             numero_siren_siret_uai='80295478500028',
             adresse_uai='12 rue des bois',
             boite_postale_uai='755484',
             code_postal_uai='75015',
             localite_acheminement_uai='truc',
             secteur_public_prive='PU',
             ministere_tutelle='1',
             categorie_juridique='36',
             site_web='sitequidechire.com',
             coordonnee_x='0.156465',
             coordonnee_y='6.3454')
        result = InstitutionSnapshotRepository.get('0802145Y')
        self.assertEqual(institution, result)

    def test_update(self):
        institution = InstitutionSnapshotRepository.create(
             numero_uai='0802145Y',
             sigle_uai='TEST',
             patronyme_uai='TEST',
             date_ouverture='2012-02-03',
             date_fermeture='2012-02-04',
             numero_siren_siret_uai='80295478500028',
             adresse_uai='12 rue des bois',
             boite_postale_uai='755484',
             code_postal_uai='75015',
             localite_acheminement_uai='truc',
             secteur_public_prive='PU',
             ministere_tutelle='1',
             categorie_juridique='36',
             site_web='sitequidechire.com',
             coordonnee_x='0.156465',
             coordonnee_y='6.3454')
        repository = InstitutionSnapshotRepository()
        update = InstitutionSnapshotRepository.update(
            repository, numero_uai='0802145Y', site_web='nouveausite')
        self.assertEqual(institution, update)
        self.assertEqual(update.site_web, 'nouveausite')
