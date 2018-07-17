"""
Define the REST verbs relative to the institutions
"""
import os
import requests
from flask import request
from flasgger import swag_from
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import Argument
from flask.json import jsonify
from repositories import BceInstitutionRepository
from util import parse_params, bad_request
from util.authorized import authorized


def delete_institution(id_esr, header):
    url = os.getenv('INSTITUTION_URL')+'institutions/' + str(id_esr)
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    headers = {'Authorization': header}
    response = requests.delete(url, proxies=proxyDict, headers=headers)
    return response.status_code


class BceInstitutionResource(Resource):
    """ Verbs relative to the institutions """

    @staticmethod
    @swag_from('../swagger/institution/GET.yml')
    def get(uai):
        """ Return an institution key information based on its uai number """
        institution = BceInstitutionRepository.get(uai=uai)
        if institution:
            return jsonify({'institution': institution.json})
        return bad_request('institution not found in database')

    @staticmethod
    @parse_params(
        Argument(
            'is_institution',
            location='json',
            required=True,
        ),
    )
    @swag_from('../swagger/institution/POST.yml')
    @authorized
    def post(uai, is_institution):
        """ Create an institution based on the sent information """
        existing_institution = BceInstitutionRepository.get(uai=uai)
        if existing_institution:
            return bad_request('duplicate value for uai number')
        if not (is_institution == 'False' or is_institution == 'True'):
            return bad_request('is_institution must be a boolean')
        institution = BceInstitutionRepository.create(
            uai=uai,
            is_institution=is_institution,
        )
        if institution:
            return jsonify({'institution': institution.json})
        return bad_request('unable to create the institution')

    @staticmethod
    @authorized
    @parse_params(
        Argument(
            'is_institution',
            location='json',
            required=True,
        ),
        Argument(
            'id_esr',
            location='json',
            required=True
        ),
    )
    @swag_from('../swagger/institution/PUT.yml')
    def put(uai, is_institution, id_esr):
        """ Update an user based on the sent information """
        if not (is_institution == 'False' or is_institution == 'True'):
            return bad_request('is_institution must be a boolean')
        if is_institution == 'False':
            response = delete_institution(
                id_esr, request.headers['Authorization'])
            if not response == 200:
                return bad_request('unable to delete id_esr')
        repository = BceInstitutionRepository()
        institution = repository.update(
                uai=uai,
                is_institution=is_institution,
        )
        if institution:
            return jsonify({'institution': institution.json})
        return jsonify({'message': 'institution deleted'})
