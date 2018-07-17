"""
Define the REST verbs relative to the institutions
"""
from flasgger import swag_from
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import Argument
from flask.json import jsonify

from repositories import SireneInstitutionRepository
from util import parse_params, bad_request
from util.authorized import authorized


class SireneInstitutionResource(Resource):
    """ Verbs relative to the siren institutions """

    @staticmethod
    @swag_from('../swagger/institution/GET.yml')
    def get(siret):
        """ Return a siren institution key information based on its siret """
        institution = SireneInstitutionRepository.get(siret=siret)
        if institution:
            return jsonify({'institution': institution.to_dict()})
        return bad_request('sirene institution not found in database')

    @staticmethod
    @parse_params(
        Argument(
            'date_maj',
            location='json',
            required=True,
            help='The last update date of the institution.'
        ),
    )
    @swag_from('../swagger/institution/POST.yml')
    @authorized
    def post(siret, date_maj):
        """ Create a siren institution based on the sent information """
        existing_institution = SireneInstitutionRepository.get(siret=siret)
        if existing_institution:
            return bad_request('duplicate value for uai_number')
        institution = SireneInstitutionRepository.create(
            siret=siret,
            date_maj=date_maj
        )
        if institution:
            return jsonify({'institution': institution.to_dict()})
        return bad_request('unable to create the institution')

    @staticmethod
    @authorized
    @parse_params(
        Argument(
            'date_maj',
            location='json',
            required=True,
            help='The last update date of the institution.'
        ),
    )
    @swag_from('../swagger/institution/PUT.yml')
    def put(siret, date_maj):
        """ Update a siren institution based on the sent information """
        repository = SireneInstitutionRepository()
        institution = repository.update(
            siret=siret,
            date_maj=date_maj
        )

        if institution:
            return jsonify({'institution': institution.to_dict()})
        return jsonify({'message': 'institution deleted'})
