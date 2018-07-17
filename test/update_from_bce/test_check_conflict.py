import unittest
from datetime import datetime
from models.abc import db
from server import server
from unittest.mock import patch

from tasks.check_conflict import (
    check_for_bce_conflict, get_esr_value_from_bce, check_for_all_bce_conflict,
    check_for_all_bce_conflict_with_snapshot)
from tasks.seed_database_bridge import seed_database_bridge
from repositories import ConflictRepository, BceSnapshotRepository


class TestCheckConflict(unittest.TestCase):

    esr_institution = {
        "id": 2736,
        "date_start": "1997-09-01",
        "date_end": "2009-08-31",
        "name": {
            "id": 2736,
            "status": "active",
            "text": "INST PR  DES METIERS SANTE",
            "initials": "INST PR  DES METIERS SANTE",
            "date_start": "2018-06-01",
            "date_end": None
        },
        "address": {
            "id": 2543,
            "business_name": "INST PR  DES METIERS SANTE",
            "address_1": "CHEMIN LA PRAIRIE PROLONGEE",
            "address_2": None,
            "zip_code": "74000",
            "city": "ANNECY",
            "country": "France",
            "phone": "0450451391",
            "latitude": 45.892912,
            "longitude": 6.120518,
            "date_start": "2018-06-01",
            "date_end": None,
            "status": "active"
        },
        "links": [],
        "codes": [
            {
                "id": 4333,
                "content": "38416491900027",
                "category": "siret",
                "date_start": None,
                "date_end": None,
                "status": "active"
            },
            {
                "id": 4332,
                "content": "0741574J",
                "category": "uai",
                "date_start": None,
                "date_end": None,
                "status": "active"
            }
        ],
        "tags": [
            {
                "id": 7,
                "short_label": "EDUC NAT",
                "long_label": "ministere de l'education nationale",
                "category": "ministere tutelle"
            },
            {
                "id": 36,
                "short_label": "PRIVE",
                "long_label": "secteur prive",
                "category": "secteur public prive"
            },
            {
                "id": 123,
                "short_label": "ENTR PUB",
                "long_label": "gere par une entreprise publique",
                "category": "catégorie juridique"
            }
        ]
    }

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('tasks.check_conflict.get_esr_value', return_value='esr_value')
    def test_for_check_conflict_same_value(self, mock_function):
        check_for_bce_conflict('0802145X', 'field_1', 'esr_value', {'id': 1})
        result = ConflictRepository.getConflictsByInstitution(id_esr=1)
        self.assertEqual(len(result), 0)

    @patch('tasks.check_conflict.get_esr_value', return_value='esr_value')
    def test_for_check_conflict_different_value(self, mock_function):
        check_for_bce_conflict('0802145X', 'field_1', 'bce_value', {'id': 1})
        result = ConflictRepository.getConflictsByInstitution(id_esr=1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].source_id, '0802145X')
        self.assertEqual(result[0].field_name, 'field_1')
        self.assertEqual(result[0].new_value, 'bce_value')
        self.assertEqual(result[0].current_value, 'esr_value')

    def test_get_esr_value_from_bce(self):
        seed_database_bridge()

        sigle_uai = get_esr_value_from_bce('sigle_uai', self.esr_institution)
        date_ouverture = get_esr_value_from_bce('date_ouverture', self.esr_institution)
        numero_siren_siret_uai = get_esr_value_from_bce('numero_siren_siret_uai',
                                                        self.esr_institution)
        adresse_uai = get_esr_value_from_bce('adresse_uai', self.esr_institution)
        secteur_public_prive = get_esr_value_from_bce('secteur_public_prive',
                                                      self.esr_institution)
        site_web = get_esr_value_from_bce('site_web', self.esr_institution)
        numero_uai = get_esr_value_from_bce('numero_uai', self.esr_institution)

        self.assertEqual(sigle_uai, "INST PR  DES METIERS SANTE")
        self.assertEqual(date_ouverture, "1997-09-01")
        self.assertEqual(numero_siren_siret_uai, "38416491900027")
        self.assertEqual(adresse_uai, "CHEMIN LA PRAIRIE PROLONGEE")
        self.assertEqual(secteur_public_prive, 36)
        self.assertEqual(site_web, None)
        self.assertEqual(numero_uai, "0741574J")

    @patch('tasks.check_conflict.check_for_bce_conflict')
    def test_check_for_all_bce_conflict(self, mock_function):

        check_for_all_bce_conflict(
                "0741574J", "INST PR  DES METIERS SANTE", "METIERS SANTE", "1997-09-01", None,
                "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
                " ", "ANNECY", None,
                12, 20, 1,
                "test.com", 123, self.esr_institution)
        self.assertEqual(mock_function.called, True)
        self.assertEqual(mock_function.call_count, 15)

    @patch('tasks.check_conflict.check_for_bce_conflict')
    def test_check_for_all_conflict_with_snapshot_with_same_values(self, mock_function):
        snapshot = BceSnapshotRepository.create(
            "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
            " ", "ANNECY", None,
            'PU', '20', '1',
            "test.com", '123')
        check_for_all_bce_conflict_with_snapshot(
            "0741574J", "MS", "METIERS SANTE", datetime(1997, 9, 1, 0, 0), None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
            " ", "ANNECY", None,
            'PU', '20', '1',
            "test.com", '123', self.esr_institution, snapshot)
        self.assertEqual(mock_function.called, False)

    @patch('tasks.check_conflict.check_for_bce_conflict')
    def test_check_for_all_conflict_with_snapshot_with_different_values(
            self, mock_function):
        snapshot = BceSnapshotRepository.create(
            "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY", " ",
            "ANNECY", None, 'PU', '20', '1', "test.com")
        check_for_all_bce_conflict_with_snapshot(
            "0741574J", "MS", "METIERS SANTE", datetime(1997, 9, 1, 0, 0), datetime(2018, 9, 1, 0, 0),
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
            " ", "ANNECY", None,
            'PU', '20', '1',
            "test.com", '123', self.esr_institution, snapshot)
        self.assertEqual(mock_function.called, True)
        self.assertEqual(mock_function.call_count, 2)
