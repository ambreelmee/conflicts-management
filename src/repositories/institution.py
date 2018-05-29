""" Defines the Institution repository """

from models import Institution


class InstitutionRepository:
    """ The repository for the institution model """

    @staticmethod
    def get(uai_number):
        """ Query an insitution by its uai_number """
        return Institution.query.filter_by(
            uai_number=uai_number,
        ).first()

    def update(self, uai_number, is_institution):
        """ Update an institution's status """
        institution = self.get(uai_number)
        institution.is_institution = is_institution

        return institution.save()

    @staticmethod
    def create(uai_number, is_institution=True):
        """ Create a new institution """
        institution = Institution(
            uai_number=uai_number,
            is_institution=is_institution)

        return institution.save()
