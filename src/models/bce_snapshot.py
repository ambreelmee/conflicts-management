"""
Define the InstitutionSnapshot model
"""
from . import db
from .abc import BaseModel


class BceSnapshot(db.Model, BaseModel):
    """ The InstitutionSnapshot model """
    __tablename__ = 'bce_snapshot'
    uai = db.Column(db.String(8), primary_key=True)
    sigle = db.Column(db.String(14))
    patronyme = db.Column(db.String(30))
    date_ouverture = db.Column(db.DateTime)
    date_fermeture = db.Column(db.DateTime)
    numero_siren_siret = db.Column(db.String(14))
    adresse = db.Column(db.String(32))
    boite_postale = db.Column(db.String(7))
    code_postal = db.Column(db.String(5))
    localite_acheminement = db.Column(db.String(32))
    numero_telephone = db.Column(db.String(13))
    secteur_public_prive = db.Column(db.String(2))
    ministere_tutelle = db.Column(db.String(2))
    categorie_juridique = db.Column(db.String(3))
    site_web = db.Column(db.String(100))
    commune = db.Column(db.String(5))

    def __init__(self,
                 categorie_juridique,
                 ministere_tutelle,
                 uai,
                 sigle,
                 secteur_public_prive,
                 date_ouverture,
                 date_fermeture,
                 patronyme,
                 adresse,
                 boite_postale,
                 code_postal,
                 localite_acheminement,
                 numero_siren_siret,
                 numero_telephone,
                 site_web,
                 commune):
        """ Create a new institutionSnapshot """
        self.categorie_juridique = categorie_juridique
        self.ministere_tutelle = ministere_tutelle
        self.uai = uai
        self.sigle = sigle
        self.secteur_public_prive = secteur_public_prive
        self.date_ouverture = date_ouverture
        self.date_fermeture = date_fermeture
        self.patronyme = patronyme
        self.adresse = adresse
        self.boite_postale = boite_postale
        self.code_postal = code_postal
        self.localite_acheminement = localite_acheminement
        self.numero_siren_siret = numero_siren_siret
        self.numero_telephone = numero_telephone
        self.site_web = site_web
        self.commune = commune

    def to_dict(self):
        """ Return the Conflict model as a python dictionary """
        return {
            'categorie_juridique': self.categorie_juridique,
            'ministere_tutelle': self.ministere_tutelle,
            'uai': self.uai,
            'sigle': self.sigle,
            'secteur_public_prive': self.secteur_public_prive,
            'date_ouverture': self.date_ouverture,
            'date_fermeture': self.date_fermeture,
            'patronyme': self.patronyme,
            'adresse': self.adresse,
            'boite_postale': self.boite_postale,
            'code_postal': self.code_postal,
            'localite_acheminement': self.localite_acheminement,
            'numero_siren_siret': self.numero_siren_siret,
            'numero_telephone': self.numero_telephone,
            'site_web': self.site_web,
            'commune': self.commune,
        }