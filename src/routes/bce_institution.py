"""
Defines the blueprint for the institutions
"""
from flask import Blueprint
from flask.ext.restful import Api

from resources import BceInstitutionResource


BCE_INSTITUTION_BLUEPRINT = Blueprint('bce_institution', __name__)
Api(BCE_INSTITUTION_BLUEPRINT).add_resource(
    BceInstitutionResource,
    '/bce_institutions/<string:uai>')
