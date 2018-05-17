"""
Defines the blueprint for the conflicts
"""
from flask import Blueprint
from flask.ext.restful import Api

from resources import ConflictResource


CONFLICT_BLUEPRINT = Blueprint('conflict', __name__)
Api(CONFLICT_BLUEPRINT).add_resource(
    ConflictResource,
    '/conflict/<string:id_path>')
