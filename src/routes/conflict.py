"""
Defines the blueprint for the conflicts
"""
from flask import Blueprint
from flask.ext.restful import Api

from resources import ConflictResource
from resources import ConflictsResource


CONFLICT_BLUEPRINT = Blueprint('conflict', __name__)
Api(CONFLICT_BLUEPRINT).add_resource(ConflictResource, '/conflicts/<string:id_path>')
Api(CONFLICT_BLUEPRINT).add_resource(ConflictsResource, '/conflicts')
