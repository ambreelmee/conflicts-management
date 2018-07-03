"""
Define the Institution model
"""
from . import db
from .abc import BaseModel


class BceInstitution(db.Model, BaseModel):
    """ The Institution model """
    __tablename__ = 'bce_institution'

    uai = db.Column(db.String(20), primary_key=True)
    # classify institutions from bce
    # depending on whether they should be in dataESR or not
    is_institution = db.Column(db.Boolean, nullable=False)

    def __init__(self, uai, is_institution):
        """ Create a new institution """
        self.uai = uai
        self.is_institution = is_institution

    def to_dict(self):
        """ Return the Institution model as a python dictionary """
        return {
            'uai': self.uai,
            'is_institution': self.is_institution,
        }