
""" Defines the Institution repository """

import os
import requests
from models import Institution


def delete_institution(id_esr, header):
    url = os.getenv('INSTITUTION_URL')+'institutions/' + str(id_esr)
    proxyDict = {"http": os.getenv('HTTP_PROXY')}
    headers = {'Authorization': header}
    response = requests.delete(url, proxies=proxyDict, headers=headers)


class InstitutionRepository:
    """ The repository for the institution model """

    @staticmethod
    def get(uai_number):
        """ Query an insitution by its uai_number """
        return Institution.query.filter_by(
            uai_number=uai_number,
        ).first()

    def update(self, uai_number, is_institution, id_esr, header):
        """ Update an institution's status """
        institution = self.get(uai_number)
        if is_institution == 'True':
            institution.is_institution = is_institution
            return institution.save()
        try:
            delete_institution(id_esr, header)
            institution.is_institution = is_institution
            return institution.save()
        except:
            raise

    @staticmethod
    def create(uai_number, is_institution=True):
        """ Create a new institution """
        institution = Institution(
            uai_number=uai_number,
            is_institution=is_institution)

        return institution.save()
