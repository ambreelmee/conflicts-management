import unittest

from server import server
from models.abc import db
from repositories import BceSnapshotRepository


class TestBceSnapshot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create(self):
        institution = BceSnapshotRepository.create(
             uai='0802145Y',
             sigle='TEST',
             patronyme='TEST',
             date_ouverture='2012-02-03',
             date_fermeture='2012-02-04',
             numero_siren_siret='80295478500028',
             adresse='12 rue des bois',
             boite_postale='755484',
             code_postal='75015',
             localite_acheminement='truc',
             secteur_public_prive='PU',
             ministere_tutelle='1',
             categorie_juridique='36',
             site_web='sitequidechire.com')
        result = BceSnapshotRepository.get('0802145Y')
        self.assertEqual(institution, result)

    def test_update(self):
        institution = BceSnapshotRepository.create(
             uai='0802145Y',
             sigle='TEST',
             patronyme='TEST',
             date_ouverture='2012-02-03',
             date_fermeture='2012-02-04',
             numero_siren_siret='80295478500028',
             adresse='12 rue des bois',
             boite_postale='755484',
             code_postal='75015',
             localite_acheminement='truc',
             secteur_public_prive='PU',
             ministere_tutelle='1',
             categorie_juridique='36',
             site_web='sitequidechire.com')
        repository = BceSnapshotRepository()
        update = BceSnapshotRepository.update(repository, uai='0802145Y', site_web='nouveausite')
        self.assertEqual(institution, update)
        self.assertEqual(update.site_web, 'nouveausite')
