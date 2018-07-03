"""
Define the InstitutionSnapshot model
"""
from . import db
from .abc import BaseModel


class SireneSnapshot(db.Model, BaseModel):
    """ The InstitutionSnapshot model """
    __tablename__ = 'sirene_snapshot'

    siret = db.Column(db.String(20), primary_key=True)
    business_name = db.Column(db.String(40))
    address_1 = db.Column(db.String(40))
    address_2 = db.Column(db.String(40))
    zip_code = db.Column(db.String(5))
    city = db.Column(db.String(40))
    country = db.Column(db.String(40))
    city_code = db.Column(db.String(20))
    naf = db.Column(db.String(5))
    date_ouverture = db.Column(db.DateTime)
    tranche_effectif = db.Column(db.String(40))

    def __init__(self,
                 siret,
                 business_name,
                 address_1,
                 address_2,
                 zip_code,
                 city,
                 country,
                 city_code,
                 naf,
                 date_ouverture,
                 tranche_effectif):
        """ Create a new institutionSnapshot """
        self.siret = siret
        self.business_name = business_name
        self.address_1 = address_1
        self.address_2 = address_2
        self.zip_code = zip_code
        self.city = city
        self.country = country
        self.city_code = city_code
        self.naf = naf
        self.date_ouverture = date_ouverture
        self.tranche_effectif = tranche_effectif

    def to_dict(self):
        """ Return the Conflict model as a python dictionary """
        return {
            'siret': self.siret,
            'business_name': self.business_name,
            'address_1': self.address_1,
            'address_2': self.address_2,
            'zip_code': self.zip_code,
            'city': self.city,
            'country': self.country,
            'city_code': self.city_code,
            'naf': self.naf,
            'date_ouverture': self.date_ouverture,
            'tranche_effectif': self.tranche_effectif
        }
