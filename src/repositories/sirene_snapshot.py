""" Defines the InstitutionSnapshot repository """

from models import SireneSnapshot


class SireneSnapshotRepository:
    """ The repository for the institutionSnapshot model """

    @staticmethod
    def get(siret):
        """ Query an insitution's snapshot by its uai_number """
        return SireneSnapshot.query.filter_by(
            siret=siret,
        ).first()

    def update(self,
               siret,
               business_name=None,
               address_1=None,
               address_2=None,
               zip_code=None,
               city=None,
               country=None,
               city_code=None,
               naf=None,
               date_ouverture=None,
               tranche_effectif=None):

        """ Update an institution's snapshot """
        institution = self.get(siret)
        if business_name:
            institution.business_name = business_name
        if address_1:
            institution.address_1 = address_1
        if address_2:
            institution.address_2 = address_2
        if zip_code:
            institution.zip_code = zip_code
        if city:
            institution.city = city
        if country:
            institution.country = country
        if city_code:
            institution.city_code = city_code
        if naf:
            institution.naf = naf
        if date_ouverture:
            institution.date_ouverture = date_ouverture
        if tranche_effectif:
            institution.tranche_effectif = tranche_effectif

        return institution.save()

    @staticmethod
    def create(self,
               siret,
               business_name=None,
               address_1=None,
               address_2=None,
               zip_code=None,
               city=None,
               country=None,
               city_code=None,
               naf=None,
               date_ouverture=None,
               tranche_effectif=None):
        """ Create a new institution snapshot """
        institution = SireneSnapshot(
            siret = siret,
            business_name = business_name,
            address_1 = address_1,
            address_2 = address_2,
            zip_code = zip_code,
            city = city,
            country = country,
            city_code = city_code,
            naf = naf,
            date_ouverture = date_ouverture,
            tranche_effectif = tranche_effectif)

        return institution.save()
