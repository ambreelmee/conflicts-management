"""
Define the ConnectionSnapshot model
"""
from . import db
from .abc import BaseModel


class ConnectionSnapshot(db.Model, BaseModel):
    """ The ConnectionSnapshot model """
    __tablename__ = 'connectionSnapshot'
    id = db.Column(db.Integer, primary_key=True)
    numero_uai = db.Column(db.String(8))
    numero_uai_rattachee = db.Column(db.String(8))
    type_rattachement = db.Column(db.String(2))
    date_ouverture = db.Column(db.DateTime)
    date_fermeture = db.Column(db.DateTime)

    def __init__(self,
                 numero_uai,
                 numero_uai_rattachee,
                 type_rattachement,
                 date_ouverture,
                 date_fermeture):
        """ Create a new connectionSnapshot """
        self.numero_uai = numero_uai
        self.numero_uai_rattachee = numero_uai_rattachee
        self.type_rattachement = type_rattachement
        self.date_ouverture = date_ouverture
        self.date_fermeture = date_fermeture

    def to_dict(self):
        """ Return the Conflict model as a python dictionary """
        return {
            'id': self.id,
            'numero_uai': self.numero_uai,
            'numero_uai_rattachee': self.numero_uai_rattachee,
            'type_rattachement': self.type_rattachement,
            'date_ouverture': self.date_ouverture,
            'date_fermeture': self.date_fermeture,
        }
