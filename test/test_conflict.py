import unittest
import json

from server import server
from models.abc import db
from repositories import ConflictRepository


class TestConflict(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        conflict_1 = ConflictRepository.create(
              id_esr=23,
              uai_number='0802145X',
              field_name='address_1',
              current_value='12 rue des bois',
              new_value='36 rue des belles feuilles',
              active=True)
        conflict_2 = ConflictRepository.create(
              id_esr=23,
              uai_number='0802145X',
              field_name='address_2',
              current_value='2ème étage',
              new_value='Batiment B',
              active=True)
        response = self.client.get(
            '/application/conflict/23',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data.decode('utf8'))
        self.assertEqual(response_json,
                         [conflict_1.to_dict(), conflict_2.to_dict()])

    def test_update(self):
        """ The PUT on `/conflict` should update an conflict's status """
        conflict = ConflictRepository.create(
              id_esr=12,
              uai_number='0802145Y',
              field_name='address_1',
              current_value='12 rue des vignes',
              new_value='36 rue des belles terres',
              active=True)
        response = self.client.put(
            '/application/conflict/' + str(conflict.id),
            content_type='application/json',
            data=json.dumps({
                'active': False
            })
        )

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf8'))
        self.assertEqual(
            response_json,
            {'conflict': conflict.to_dict()})
        updated_conflict = ConflictRepository.get(id=conflict.id)
        self.assertEqual(updated_conflict.active, False)
