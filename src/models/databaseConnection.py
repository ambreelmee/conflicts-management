"""
Define the DatabaseConnection model
"""
from . import db
from .abc import BaseModel


class DatabaseConnection(db.Model, BaseModel):
    """ The DatabaseConnection model """
    __tablename__ = 'database_connection'
    bce_field = db.Column(db.String(30), primary_key=True)
    bloc = db.Column(db.String(30))
    value_key = db.Column(db.String(30), nullable=False)
    criterion_key = db.Column(db.String(30))
    criterion_value = db.Column(db.String(30))

    def __init__(self,
                 bce_field,
                 bloc,
                 value_key,
                 criterion_key,
                 criterion_value):
        """ Create a new DatabaseConnection """
        self.bce_field = bce_field
        self.bloc = bloc
        self.value_key = value_key
        self.criterion_key = criterion_key
        self.criterion_value = criterion_value

    def to_dict(self):
        """ Return the Conflict model as a python dictionary """
        return {
            'bce_field': self.bce_field,
            'bloc': self.bloc,
            'value_key': self.value_key,
            'criterion_key': self.criterion_key,
            'criterion_value': self.criterion_value,
        }
