"""
Define the REST verbs relative to the institutions
"""
from flasgger import swag_from
from flask import abort, request
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import Argument
from flask.json import jsonify
from repositories import InstitutionRepository
from util import parse_params
from util.authorized import authorized
from werkzeug.exceptions import BadRequest


class InstitutionResource(Resource):
    """ Verbs relative to the institutions """

    @staticmethod
    @swag_from('../swagger/institution/GET.yml')
    def get(uai_number):
        """ Return an institution key information based on its uai number """
        institution = InstitutionRepository.get(uai_number=uai_number)
        try:
            return jsonify({'institution': institution.json})
        except:
            raise BadRequest('institution not found')

    @staticmethod
    @parse_params(
        Argument(
            'is_institution',
            location='json',
            required=True,
            help='The status of the institution.'
        ),
    )
    @swag_from('../swagger/institution/POST.yml')
    @authorized
    def post(uai_number, is_institution):
        """ Create an institution based on the sent information """
        institution = InstitutionRepository.create(
            uai_number=uai_number,
            is_institution=is_institution,
        )
        return jsonify({'institution': institution.json})

    @staticmethod
    @authorized
    @parse_params(
        Argument(
            'is_institution',
            location='json',
            required=True,
            help='The status of the institution.'
        ),
        Argument(
            'id_esr',
            location='json',
            required=True
        ),
    )
    @swag_from('../swagger/institution/PUT.yml')
    def put(uai_number, is_institution, id_esr):
        """ Update an user based on the sent information """
        repository = InstitutionRepository()
        try:
            institution = repository.update(
                uai_number=uai_number,
                is_institution=is_institution,
                id_esr=id_esr,
                header=request.headers['Authorization']
            )
        except:
            print("An error occured")
            abort(404)
        return jsonify({'institution': institution.json})
