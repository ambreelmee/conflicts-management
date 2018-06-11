import unittest
import json
import os
from unittest.mock import patch
from server import server
from models.abc import db
from models import Institution
from repositories import InstitutionRepository
from requests import HTTPError


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
    def test_update_true(self, mock_decorator):
        """ The PUT on `/institution` should update an institution's status
        if it is updated from False to True"""
        InstitutionRepository.create(
            uai_number='0802145Z', is_institution=False)
        response = self.client.put(
            '/application/institution/0802145Z',
            content_type='application/json',
            headers={'Authorization': 'Bearer token'},
            data=json.dumps({
                'is_institution': True,
                'id_esr': 4
            })
        )
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf8'))
        self.assertEqual(
            response_json,
            {'institution':
                {'uai_number': '0802145Z', 'is_institution': True}}
            )
        institution = InstitutionRepository.get(uai_number='0802145Z')
        self.assertEqual(institution.is_institution, True)

    @patch('requests.delete', side_effect=HTTPError())
    @patch('util.authorized.validate_token', return_value=True)
    def test_update_false_failed(self, mock_decorator, mock_request):
        """ The PUT on `/institution` should not update an institution's status
        if an error accured when deleting the institution"""
        InstitutionRepository.create(
            uai_number='0802145Z', is_institution=True)
        headers = {'Authorization': 'Bearer token'}
        response = self.client.put(
            '/application/institution/0802145Z',
            content_type='application/json',
            headers=headers,
            data=json.dumps({
                'is_institution': False,
                'id_esr': 4
            })
        )

        self.assertEqual(mock_request.called, True)
        url = ((os.getenv('INSTITUTION_URL')) + 'institutions/4',)
        args, kwargs = mock_request.call_args
        self.assertEqual(args, url)
        self.assertEqual(response.status_code, 404)

        institution = InstitutionRepository.get(uai_number='0802145Z')
        self.assertEqual(institution.is_institution, True)

    @patch('requests.delete')
    @patch('util.authorized.validate_token', return_value=True)
    def test_update_false_success(self, mock_decorator, mock_request):
        """ The PUT on `/institution` should update an institution's status
        and delete the institution in dataESR """
        InstitutionRepository.create(
            uai_number='0802145Z', is_institution=True)
        headers = {'Authorization': 'Bearer token'}
        response = self.client.put(
            '/application/institution/0802145Z',
            content_type='application/json',
            headers=headers,
            data=json.dumps({
                'is_institution': False,
                'id_esr': 4
            })
        )
        self.assertEqual(mock_request.called, True)
        url = ((os.getenv('INSTITUTION_URL')) + 'institutions/4',)
        args, kwargs = mock_request.call_args
        self.assertEqual(args, url)
        self.assertEqual(response.status_code, 200)

        institution = InstitutionRepository.get(uai_number='0802145Z')
        self.assertEqual(institution.is_institution, False)
