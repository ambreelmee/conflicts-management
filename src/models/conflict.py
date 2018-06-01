"""
Define the Conflict model
"""
from . import db
from .abc import BaseModel


class Conflict(db.Model, BaseModel):
    """ The Conflict model """
    __tablename__ = 'conflict'
    id = db.Column(db.Integer, primary_key=True)
    uai_number = db.Column(db.String(20), nullable=False)
    field_name = db.Column(db.String(50), nullable=False)
    current_value = db.Column(db.String(120), nullable=True)
    new_value = db.Column(db.String(120), nullable=True)
    active = db.Column(db.Boolean, nullable=False)
    id_esr = db.Column(db.Integer, nullable=False)

    def __init__(self,
                 uai_number,
                 field_name,
                 current_value,
                 new_value,
                 active,
                 id_esr):
        """ Create a new conflict """
        self.uai_number = uai_number
        self.field_name = field_name
        self.current_value = current_value
        self.new_value = new_value
        self.active = active
        self.id_esr = id_esr

    def to_dict(self):
        """ Return the Conflict model as a python dictionary """
        return {
            'id': self.id,
            'uai_number': self.uai_number,
            'field_name': self.field_name,
            'current_value': self.current_value,
            'new_value': self.new_value,
            'active': self.active,
            'id_esr': self.id_esr,
        }
