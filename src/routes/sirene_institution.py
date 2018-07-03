"""
Defines the blueprint for the institutions
"""
from flask import Blueprint
from flask.ext.restful import Api

from resources import SireneInstitutionResource

SIRENE_INSTITUTION_BLUEPRINT = Blueprint('sirene_institution', __name__)
Api(SIRENE_INSTITUTION_BLUEPRINT).add_resource(
    SireneInstitutionResource,
    '/sirene_institutions/<string:siret>')

