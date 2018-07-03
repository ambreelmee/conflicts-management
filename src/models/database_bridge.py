"""
Define the DatabaseConnection model
"""
from . import db
from .abc import BaseModel


class DatabaseBridge(db.Model, BaseModel):
    """ The DatabaseBridge model """
    __tablename__ = 'database_bridge'
    sirene_field = db.Column(db.String(30), primary_key=True)
    bloc = db.Column(db.String(30))
    value_key = db.Column(db.String(30), nullable=False)
    criterion_key = db.Column(db.String(30))
    criterion_value = db.Column(db.String(30))

    def __init__(self,
                 sirene_field,
                 bloc,
                 value_key,
                 criterion_key,
                 criterion_value):
        """ Create a new DatabaseBridge """
        self.sirene_field = sirene_field
        self.bloc = bloc
        self.value_key = value_key
        self.criterion_key = criterion_key
        self.criterion_value = criterion_value

    def to_dict(self):
        """ Return the DatabaseBridge model as a python dictionary """
        return {
            'sirene_field': self.sirene_field,
            'bloc': self.bloc,
            'value_key': self.value_key,
            'criterion_key': self.criterion_key,
            'criterion_value': self.criterion_value,
        }
