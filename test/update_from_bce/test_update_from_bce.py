import unittest
from models.abc import db
from server import server
from unittest.mock import patch
from tasks.update_from_bce import (
    compare_esr_without_snapshot, compare_esr_with_snapshot, update_from_bce)
from repositories import BceSnapshotRepository, BceInstitutionRepository


class TestUpdateFromBce(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('tasks.update_from_bce.get_institution_from_esr', return_value=None)
    @patch('tasks.update_from_bce.create_esr_institution', return_value=1)
    def test_compare_esr_without_snapshot_no_institution(
            self, mock_create_institution, mock_get_institution):
        count = compare_esr_without_snapshot(
            "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
            " ", "ANNECY", None,
            'PU', '20', '1',
            "test.com", '123', 'token', [], [],
            0)
        snapshot = BceSnapshotRepository.get('0741574J')

        self.assertEqual(snapshot.sigle, 'MS')
        self.assertEqual(snapshot.patronyme, 'METIERS SANTE')

        self.assertEqual(mock_create_institution.called, True)
        args, kwargs = mock_create_institution.call_args
        expected_args = (
            'token', "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY", " ",
            "ANNECY", None, 'PU', '20', '1', "test.com", '123', [], [], 0)
        self.assertEqual(args, expected_args)
        self.assertEqual(count, 1)

    @patch('tasks.update_from_bce.get_institution_from_esr',
           return_value={'institution': {'id': 1}})
    @patch('tasks.update_from_bce.check_for_all_bce_conflict')
    def test_compare_esr_without_snapshot_institution(
            self, mock_check_conflict, mock_get_institution):
        count = compare_esr_without_snapshot(
            "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY", " ",
            "ANNECY", None, 'PU', '20', '1', "test.com", '123', 'token', [], [], 0)
        snapshot = BceSnapshotRepository.get('0741574J')

        self.assertEqual(snapshot.sigle, 'MS')
        self.assertEqual(snapshot.patronyme, 'METIERS SANTE')

        self.assertEqual(mock_check_conflict.called, True)
        args, kwargs = mock_check_conflict.call_args
        expected_args = (
            "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY", " ",
            "ANNECY", None, 'PU', '20', '1', "test.com", '123', {'id': 1})
        self.assertEqual(args, expected_args)
        self.assertEqual(count, 0)

    @patch('tasks.update_from_bce.get_institution_from_esr', return_value=None)
    @patch('tasks.update_from_bce.create_esr_institution', return_value=1)
    def test_compare_esr_with_snapshot_no_institution(
            self, mock_create_institution, mock_get_institution):
        snapshot = BceSnapshotRepository.create(
            "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY", " ",
            "ANNECY", None, 'PU', '20', '1', "test.com")
        count = compare_esr_with_snapshot(
            "0741574J", "MSE", "METIERS SANTE", "1997-09-01",
            None, "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
            " ", "ANNECY", None,
            'PU', '20', '1',
            "test.com", '123', 'token', [], [],
            0, snapshot)

        self.assertEqual(mock_create_institution.called, True)
        args, kwargs = mock_create_institution.call_args
        expected_args = (
            'token', "0741574J", "MSE", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY", " ",
            "ANNECY", None, 'PU', '20', '1', "test.com", '123', [], [], 0)
        self.assertEqual(args, expected_args)
        self.assertEqual(count, 1)

        snapshot_updated = BceSnapshotRepository.get('0741574J')

        self.assertEqual(snapshot_updated.sigle, 'MSE')

    @patch('tasks.update_from_bce.get_institution_from_esr',
           return_value={'institution': {'id': 1}})
    @patch('tasks.update_from_bce.check_for_all_bce_conflict_with_snapshot')
    def test_compare_esr_with_snapshot_institution(
            self, mock_check_conflict, mock_get_institution):
        snapshot = BceSnapshotRepository.create(
            "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY", " ",
            "ANNECY", None, 'PU', '20', '1', "test.com", '123')
        count = compare_esr_with_snapshot(
            "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
            " ", "ANNECY", None,
            'PU', '20', '1',
            "test.com", '123', 'token', [], [],
            0, snapshot)

        self.assertEqual(mock_check_conflict.called, True)
        args, kwargs = mock_check_conflict.call_args
        expected_args = (
            "0741574J", "MS", "METIERS SANTE", "1997-09-01", None,
            "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY", " ",
            "ANNECY", None, 'PU', '20', '1', "test.com", '123', {'id': 1}, snapshot)
        self.assertEqual(args, expected_args)
        self.assertEqual(count, 0)

    @patch('tasks.update_from_bce.compare_esr_without_snapshot',
           return_value=1)
    @patch('tasks.update_from_bce.get_code_categories')
    @patch('tasks.update_from_bce.get_link_categories')
    @patch('tasks.update_from_bce.authenticate',
           return_value={'access_token': 'token'})
    @patch("psycopg2.connect")
    def test_update_from_bce_no_institution(
            self, mock_connect, mock_auth, mock_links, mock_codes,
            mock_comparison):
        result = [
            ["0741574J", '400', "MS", "METIERS SANTE", "1997-09-01", None,
             "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
             " ", "ANNECY", None, 'PU', '20', '1', "test.com", '123'],
            ["0741574L", '320', "MU", "METIERS SANTE UNIV", "1997-09-01", None,
             "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
             " ", "ANNECY", None, 'PU', '20', '1', "test.com", '123']]
        curs = mock_connect.return_value.cursor
        curs.return_value.__enter__.return_value.__iter__.return_value = result
        count = update_from_bce()
        instit1 = BceInstitutionRepository.get('0741574J')
        instit2 = BceInstitutionRepository.get('0741574L')

        self.assertEqual(instit1.is_institution, True)
        self.assertEqual(instit2.is_institution, False)
        self.assertEqual(mock_comparison.called, True)
        self.assertEqual(mock_comparison.call_count, 1)
        self.assertEqual(count, {'bce_count': 2, 'esr_count': 1})

    @patch('tasks.update_from_bce.compare_esr_with_snapshot',
           return_value=0)
    @patch('tasks.update_from_bce.compare_esr_without_snapshot',
           return_value=0)
    @patch('tasks.update_from_bce.get_code_categories')
    @patch('tasks.update_from_bce.get_link_categories')
    @patch('tasks.update_from_bce.authenticate',
           return_value={'access_token': 'token'})
    @patch("psycopg2.connect")
    def test_update_from_bce_institution(
            self, mock_connect, mock_auth, mock_links, mock_codes,
            mock_comparison_without_snapshot, mock_comparison_with_snapshot):
        BceInstitutionRepository.create('0741574I', True)
        BceSnapshotRepository.create('0741574I')
        BceInstitutionRepository.create('0741574J', True)
        BceInstitutionRepository.create('0741574L', False)
        query = """ SELECT numero_uai, nature_uai, sigle_uai, patronyme_uai,
                date_ouverture, date_fermeture, numero_siren_siret_uai,
                adresse_uai, boite_postale_uai, code_postal_uai,
                localite_acheminement_uai, numero_telephone_uai,
                secteur_public_prive, ministere_tutelle, categorie_juridique,
                site_web, commune FROM bce_uai"""
        result = [
            ["0741574I", '400', "MS", "METIERS SANTE", "1997-09-01", None,
             "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
             " ", "ANNECY", None, 'PU', '20', '1', "test.com", '123'],
            ["0741574J", '400', "MS", "METIERS SANTE", "1997-09-01", None,
             "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
             " ", "ANNECY", None, 'PU', '20', '1', "test.com", '123'],
            ["0741574L", '320', "MU", "METIERS SANTE UNIV", "1997-09-01", None,
             "38416491900027", "CHEMIN LA PRAIRIE PROLONGEE", "ANNECY",
             " ", "ANNECY", None, 'PU', '20', '1', "test.com", '123']]
        curs = mock_connect.return_value.cursor
        curs.return_value.__enter__.return_value.__iter__.return_value = result
        count = update_from_bce()
        execute = curs.return_value.__enter__.return_value.execute
        execute.assert_called_once_with(query)
        self.assertEqual(mock_comparison_without_snapshot.called, True)
        self.assertEqual(mock_comparison_without_snapshot.call_count, 1)
        self.assertEqual(mock_comparison_with_snapshot.called, True)
        self.assertEqual(mock_comparison_with_snapshot.call_count, 1)
        self.assertEqual(count, {'bce_count': 0, 'esr_count': 0})
