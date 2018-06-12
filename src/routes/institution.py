"""
Defines the blueprint for the institutions
"""
from flask import Blueprint
from flask.ext.restful import Api

from resources import InstitutionResource


INSTITUTION_BLUEPRINT = Blueprint('institution', __name__)
Api(INSTITUTION_BLUEPRINT).add_resource(
    InstitutionResource,
    '/institutions/<string:uai_number>')
