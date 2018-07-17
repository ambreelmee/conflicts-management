import unittest
import json
import os
from unittest.mock import patch
from server import server
from models.abc import db
from models import BceInstitution
from repositories import BceInstitutionRepository


def mocked_requests_delete(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(None, 200)


def mocked_requests_delete_failed(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(None, 400)


class TestBceInstitution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get(self):
        BceInstitutionRepository.create(
            uai='0802145X', is_institution=True)
        response = self.client.get(
            '/api/bce_institutions/0802145X',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(response.data.decode('utf8'))
        self.assertEqual(
            response_json,
            {'institution': {'uai': '0802145X', 'is_institution': True}}
        )

    @patch('util.authorized.validate_token', return_value=True)
    def test_create(self, mock_decorator):
        """ The POST on `/institution` should create an institution """
        response = self.client.post(
            '/api/bce_institutions/0802145Y',
            content_type='application/json',
            headers={'Authorization': 'Bearer token'},
            data=json.dumps({
                'is_institution': True
            }))
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode('utf8'))
        self.assertEqual(
            response_json,
            {'institution': {'uai': '0802145Y', 'is_institution': True}}
        )
        self.assertEqual(BceInstitution.query.count(), 1)

    @patch('util.authorized.validate_token', return_value=True)
    def test_update_true(self, mock_decorator):
        """ The PUT on `/institution` should update an institution's status
        if it is updated from False to True"""
        BceInstitutionRepository.create(
            uai='0802145Z', is_institution=False)
        response = self.client.put(
            '/api/bce_institutions/0802145Z',
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
                {'uai': '0802145Z', 'is_institution': True}}
            )
        institution = BceInstitutionRepository.get(uai='0802145Z')
        self.assertEqual(institution.is_institution, True)

    @patch('requests.delete', side_effect=mocked_requests_delete_failed)
    @patch('util.authorized.validate_token', return_value=True)
    def test_update_false_failed(self, mock_decorator, mock_request):
        """ The PUT on `/institution` should not update an institution's status
        if an error accured when deleting the institution"""
        BceInstitutionRepository.create(uai='0802145Z', is_institution=True)
        headers = {'Authorization': 'Bearer token'}
        response = self.client.put(
            '/api/bce_institutions/0802145Z',
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
        self.assertEqual(response.status_code, 400)

        institution = BceInstitutionRepository.get(uai='0802145Z')
        self.assertEqual(institution.is_institution, True)

    @patch('requests.delete', side_effect=mocked_requests_delete)
    @patch('util.authorized.validate_token', return_value=True)
    def test_update_false_success(self, mock_decorator, mock_request):
        """ The PUT on `/institution` should update an institution's status
        and delete the institution in dataESR """
        BceInstitutionRepository.create(
            uai='0802145Z', is_institution=True)
        headers = {'Authorization': 'Bearer token'}
        response = self.client.put(
            '/api/bce_institutions/0802145Z',
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

        institution = BceInstitutionRepository.get(uai='0802145Z')
        self.assertEqual(institution.is_institution, False)
