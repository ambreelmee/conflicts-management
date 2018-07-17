"""
Define the Institution model
"""
from . import db
from .abc import BaseModel


class SireneInstitution(db.Model, BaseModel):
    """ The Sirene Institution model """
    __tablename__ = 'sirene_institution'

    siret = db.Column(db.String(20), primary_key=True)
    date_maj = db.Column(db.DateTime)

    def __init__(self, siret, date_maj):
        """ Create a new institution """
        self.siret = siret
        self.date_maj = date_maj

    def to_dict(self):
        """ Return the Institution model as a python dictionary """
        return {
            'siret': self.siret,
            'date_maj': str(self.date_maj)
        }
