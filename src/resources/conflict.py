"""
Define the REST verbs relative to the conflicts
"""
from flasgger import swag_from
from flask.ext.restful import Resource
from flask.ext.restful.reqparse import Argument
from flask.json import jsonify

from repositories import ConflictRepository
from util import parse_params
from util.authorized import authorized


class ConflictResource(Resource):
    """ Verbs relative to the conflicts """

    @staticmethod
    @swag_from('../swagger/conflict/GET.yml')
    def get(id_path):
        """ Return all conflicts for a given institutions """
        conflicts = ConflictRepository.getConflictsByInstitution(
            id_esr=id_path)
        return [conflict.to_dict() for conflict in conflicts] 

    @staticmethod
    @parse_params(
        Argument(
            'active',
            location='json',
            required=True,
            help='The status of the conflict.'
        ),
    )
    @swag_from('../swagger/conflict/PUT.yml')
    @authorized
    def put(id_path, active):
        """ Update a conflict status """
        repository = ConflictRepository()
        conflict = repository.update(
            id=id_path,
            active=active,
        )
        return jsonify({'conflict': conflict.json})
