"""
Define the InstitutionSnapshot model
"""
from . import db
from .abc import BaseModel


class InstitutionSnapshot(db.Model, BaseModel):
    """ The InstitutionSnapshot model """
    __tablename__ = 'institution_snapshot'
    numero_uai = db.Column(db.String(8), primary_key=True)
    sigle_uai = db.Column(db.String(14))
    patronyme_uai = db.Column(db.String(30))
    date_ouverture = db.Column(db.DateTime)
    date_fermeture = db.Column(db.DateTime)
    numero_siren_siret_uai = db.Column(db.String(14))
    adresse_uai = db.Column(db.String(32))
    boite_postale_uai = db.Column(db.String(7))
    code_postal_uai = db.Column(db.String(5))
    localite_acheminement_uai = db.Column(db.String(32))
    numero_telephone_uai = db.Column(db.String(13))
    secteur_public_prive = db.Column(db.String(2))
    ministere_tutelle = db.Column(db.String(2))
    categorie_juridique = db.Column(db.String(3))
    site_web = db.Column(db.String(100))

    def __init__(self,
                 categorie_juridique,
                 ministere_tutelle,
                 numero_uai,
                 sigle_uai,
                 secteur_public_prive,
                 date_ouverture,
                 date_fermeture,
                 patronyme_uai,
                 adresse_uai,
                 boite_postale_uai,
                 code_postal_uai,
                 localite_acheminement_uai,
                 numero_siren_siret_uai,
                 numero_telephone_uai,
                 site_web):
        """ Create a new institutionSnapshot """
        self.categorie_juridique = categorie_juridique
        self.ministere_tutelle = ministere_tutelle
        self.numero_uai = numero_uai
        self.sigle_uai = sigle_uai
        self.secteur_public_prive = secteur_public_prive
        self.date_ouverture = date_ouverture
        self.date_fermeture = date_fermeture
        self.patronyme_uai = patronyme_uai
        self.adresse_uai = adresse_uai
        self.boite_postale_uai = boite_postale_uai
        self.code_postal_uai = code_postal_uai
        self.localite_acheminement_uai = localite_acheminement_uai
        self.numero_siren_siret_uai = numero_siren_siret_uai
        self.numero_telephone_uai = numero_telephone_uai
        self.site_web = site_web

    def to_dict(self):
        """ Return the Conflict model as a python dictionary """
        return {
            'categorie_juridique': self.categorie_juridique,
            'ministere_tutelle': self.ministere_tutelle,
            'numero_uai': self.numero_uai,
            'sigle_uai': self.sigle_uai,
            'secteur_public_prive': self.secteur_public_prive,
            'date_ouverture': self.date_ouverture,
            'date_fermeture': self.date_fermeture,
            'patronyme_uai': self.patronyme_uai,
            'adresse_uai': self.adresse_uai,
            'boite_postale_uai': self.boite_postale_uai,
            'code_postal_uai': self.code_postal_uai,
            'localite_acheminement_uai': self.localite_acheminement_uai,
            'numero_siren_siret_uai': self.numero_siren_siret_uai,
            'numero_telephone_uai': self.numero_telephone_uai,
            'site_web': self.site_web,
        }
