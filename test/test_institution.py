import unittest
import json
from unittest.mock import patch
from server import server
from models.abc import db
from models import Institution
from repositories import InstitutionRepository

class TestInstitution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        InstitutionRepository.create(
            uai_number='0802145X', is_institution=True)
        response = self.client.get(
            '/application/institution/0802145X',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data.decode('utf8'))
        self.assertEqual(
            response_json,
            {'institution': {'uai_number': '0802145X', 'is_institution': True}}
        )

    @patch('util.authorized.validate_token', return_value=True)
    def test_create(self, mock_decorator):
        """ The POST on `/institution` should create an institution """
        response = self.client.post(
            '/application/institution/0802145Y',
            content_type='application/json',
            headers={'Authorization': 'Bearer token'},
            data=json.dumps({
                'is_institution': True
            }))
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf8'))
        self.assertEqual(
            response_json,
            {'institution': {'uai_number': '0802145Y', 'is_institution': True}}
        )
        self.assertEqual(Institution.query.count(), 1)

    @patch('util.authorized.validate_token', return_value=True)
    def test_update(self, mock_decorator):
        """ The PUT on `/institution` should update an institution's status """
        InstitutionRepository.create(
            uai_number='0802145Z', is_institution=True)
        response = self.client.put(
            '/application/institution/0802145Z',
            content_type='application/json',
            headers={'Authorization': 'Bearer token'},
            data=json.dumps({
                'is_institution': False
            })
        )

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf8'))
        self.assertEqual(
            response_json,
            {'institution':
                {'uai_number': '0802145Z', 'is_institution': False}}
        )
        institution = InstitutionRepository.get(uai_number='0802145Z')
        self.assertEqual(institution.is_institution, False)
