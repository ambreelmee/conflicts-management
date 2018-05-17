import unittest

from server import server
from models.abc import db
from repositories import ConnectionSnapshotRepository


class TestConnectionSnapshot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create(self):
        connection = ConnectionSnapshotRepository.create(
             numero_uai='0802145Y',
             numero_uai_rattachee='0802145Z',
             type_rattachement='32',
             date_ouverture='2012-02-03',
             date_fermeture='2012-02-04')
        result = ConnectionSnapshotRepository.get(connection.id)
        self.assertEqual(connection, result)

    def test_update(self):
        connection = ConnectionSnapshotRepository.create(
             numero_uai='0802145Y',
             numero_uai_rattachee='0802145Z',
             type_rattachement='32',
             date_ouverture='2012-02-03',
             date_fermeture='2012-02-04')
        repository = ConnectionSnapshotRepository()
        update = ConnectionSnapshotRepository.update(
            repository, id=connection.id, type_rattachement='12')
        self.assertEqual(connection, update)
        self.assertEqual(update.type_rattachement, '12')

    def test_get(self):
        connection_1 = ConnectionSnapshotRepository.create(
             numero_uai='0802145Y',
             numero_uai_rattachee='0802145Z',
             type_rattachement='32',
             date_ouverture='2012-02-03',
             date_fermeture='2012-02-04')
        connection_2 = ConnectionSnapshotRepository.create(
             numero_uai='0802145Y',
             numero_uai_rattachee='1234567P',
             type_rattachement='05')
        results = ConnectionSnapshotRepository.getAllConnectionsByInstitution(
            '0802145Y')
        self.assertEqual(results, [connection_1, connection_2])
