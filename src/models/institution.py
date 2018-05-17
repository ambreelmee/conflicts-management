"""
Define the Institution model
"""
from . import db
from .abc import BaseModel


class Institution(db.Model, BaseModel):
    """ The Institution model """
    __tablename__ = 'institution'

    uai_number = db.Column(db.String(20), primary_key=True)
    # classify institutions from bce
    # depending on whether they should be in dataESR or not
    is_institution = db.Column(db.Boolean, nullable=False)

    def __init__(self, uai_number, is_institution):
        """ Create a new institution """
        self.uai_number = uai_number
        self.is_institution = is_institution

    def to_dict(self):
        """ Return the Institution model as a python dictionary """
        return {
            'uai_number': self.uai_number,
            'is_institution': self.is_institution,
        }
