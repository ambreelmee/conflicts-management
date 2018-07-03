""" Defines the Institution repository """


from models import BceInstitution


class BceInstitutionRepository:
    """ The repository for the institution model """

    @staticmethod
    def get(uai):
        """ Query an BCE insitution by its uai """
        return BceInstitution.query.filter_by(uai=uai).first()

    def update(self, uai, is_institution):
        """ Update an BCE institution's status """
        institution = self.get(uai)
        if not institution:
            return None
        institution.is_institution = is_institution
        return institution.save()

    @staticmethod
    def create(uai, is_institution=True):
        """ Create a new BCE institution """
        institution = BceInstitution(
            uai=uai,
            is_institution=is_institution)

        return institution.save()
