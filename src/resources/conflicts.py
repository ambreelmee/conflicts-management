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


class ConflictsResource(Resource):
    """ Verbs relative to the conflicts """

    @staticmethod
    def get():
        """ Return all conflicts """
        conflicts = ConflictRepository.getAllConflicts()
        return [conflict.to_dict() for conflict in conflicts]   

 