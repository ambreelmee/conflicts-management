""" Defines the Institution repository """

from models import SireneInstitution


class SireneInstitutionRepository:
    """ The repository for the institution model """

    @staticmethod
    def get(siret):
        """ Query an insitution by its uai_number """
        return SireneInstitution.query.filter_by(
            siret=siret,
        ).first()

    def update(self, siret, date_maj):
        """ Update an institution's status """
        institution = self.get(siret)
        institution.date_maj = date_maj

        return institution.save()

    @staticmethod
    def create(siret, date_maj):
        """ Create a new institution """
        print('in create')
        print(date_maj)

        institution = SireneInstitution(
            siret=siret,
            date_maj=date_maj)

        return institution.save()
