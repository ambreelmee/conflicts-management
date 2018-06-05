import unittest
import os
from models.abc import db
from server import server
from unittest.mock import patch
from tasks.create_esr_institution import (
    find_category_id, create_numero_uai, create_address,
    create_ministere_tutelle, create_public_prive, create_categorie_juridique,
    create_website)
from tasks.seed_database_connection import seed_database_connection


class TestCreateEsrInstitution(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()
        seed_database_connection()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_find_codes_category_id(self):
        code_categories = [
            {"id": 1, "title": "uai"}, {"id": 2, "title": "siret"},
            {"id": 3, "title": "grid"}, {"id": 4, "title": "eter"},
            {"id": 5, "title": "wikidata"}, {"id": 6, "title": "orgref"},
            {"id": 7, "title": "isni"}, {"id": 8, "title": "funding_data"}
        ]
        siret = find_category_id(code_categories, 'numero_siren_siret_uai')
        uai = find_category_id(code_categories, 'numero_uai')
        self.assertEqual(siret, 2)
        self.assertEqual(uai, 1)

    def test_find_links_category_id(self):
        link_categories = [
            {"id": 1, "title": "website"}, {"id": 2, "title": "wikipedia"},
            {"id": 3, "title": "rss_feed"}, {"id": 4, "title": "mooc"},
            {"id": 5, "title": "facebook"}, {"id": 6, "title": "twitter"},
            {"id": 7, "title": "instagram"}, {"id": 8, "title": "youtube"}
        ]
        website = find_category_id(link_categories, 'site_web')
        self.assertEqual(website, 1)

    @patch('tasks.create_esr_institution.find_category_id', return_value=1)
    @patch('requests.post')
    def test_create_numero_uai(self, mock_post, mock_category):
        create_numero_uai("0741574J", "1", {'Authorization': 'token'}, [])
        data = {"code": {"content": "0741574J", "code_category_id": 1}}
        self.assertEqual(mock_post.called, True)
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json'], data)

    @patch('requests.post')
    def test_create_address(self, mock_post,):
        create_address('etablissement', '12 rue des bois', None, '75015',
                       'Paris', None, '2', {})
        data = {"address": {
            "business_name": "etablissement", "address_1": "12 rue des bois",
            "address_2": None, "zip_code": '75015', "city": 'Paris',
            "country": "France", "phone": None}}
        self.assertEqual(mock_post.called, True)
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json'], data)

    @patch('requests.post')
    def test_create_ministere_tutelle(self, mock_post,):
        create_ministere_tutelle("12", "3", {})
        url = ((os.getenv('INSTITUTION_URL')) + 'institutions/3/tags/14',)
        self.assertEqual(mock_post.called, True)
        args, kwargs = mock_post.call_args
        self.assertEqual(args, url)

    @patch('requests.post')
    def test_create_public_prive(self, mock_post,):
        create_public_prive('PU', '4', {})
        url = ((os.getenv('INSTITUTION_URL')) + 'institutions/4/tags/35',)
        self.assertEqual(mock_post.called, True)
        args, kwargs = mock_post.call_args
        self.assertEqual(args, url)

    @patch('requests.post')
    def test_create_categorie_juridique(self, mock_post,):
        create_categorie_juridique('258', '5', {})
        url = ((os.getenv('INSTITUTION_URL')) + 'institutions/5/tags/131',)
        self.assertEqual(mock_post.called, True)
        args, kwargs = mock_post.call_args
        self.assertEqual(args, url)

    @patch('tasks.create_esr_institution.find_category_id', return_value=1)
    @patch('requests.post')
    def test_create_website(self, mock_post, mock_category):
        create_website('monsiteweb.com', '6', {}, [])
        data = {"link": {"content": 'monsiteweb.com', 'link_category_id': 1}}
        self.assertEqual(mock_post.called, True)
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json'], data)
