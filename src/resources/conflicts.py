"""
Define the REST verbs relative to the conflicts
"""
from flask.ext.restful import Resource
from repositories import ConflictRepository


class ConflictsResource(Resource):
    """ Verbs relative to the conflicts """

    @staticmethod
    def get():
        """ Return all conflicts """
        conflicts = ConflictRepository.getAllConflicts()
        return [conflict.to_dict() for conflict in conflicts]
