"""
Define the REST verbs relative to the institutions
"""
from flasgger import swag_from
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import Argument
from flask.json import jsonify

from repositories import SireneInstitutionRepository
from util import parse_params
from util.authorized import authorized


class SireneInstitutionResource(Resource):
    """ Verbs relative to the institutions """

    @staticmethod
    @swag_from('../swagger/institution/GET.yml')
    def get(siret):
        """ Return an institution key information based on its siret """
        institution = SireneInstitutionRepository.get(siret=siret)
        return jsonify({'institution': institution.to_dict()})

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
        """ Create an institution based on the sent information """
        institution = SireneInstitutionRepository.create(
            siret=siret,
            date_maj=date_maj
        )
        return jsonify({'institution': institution.to_dict()})

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
        """ Update an user based on the sent information """
        repository = InstitutionRepository()
        institution = repository.update(
            siret=siret,
            date_maj=date_maj
        )
        return jsonify({'institution': institution.to_dict()})
