""" Defines the Conflict repository """

from models import Conflict


class ConflictRepository:
    """ The repository for the conflict model """

    @staticmethod
    def get(id):
        """ Query a conflict with its id """
        return Conflict.query.filter_by(
            id=id,
        ).one()

    @staticmethod
    def getConflictsByInstitution(id_esr):
        """ Query all conflicts for a given institution """
        return Conflict.query.filter_by(
            id_esr=id_esr,
        ).all()

    def update(self, id, active):
        """ Update a conflict's status"""
        conflict = self.get(id)
        conflict.active = active
        return conflict.save()

    @staticmethod
    def create(uai_number,
               field_name,
               current_value,
               new_value,
               active,
               id_esr):
        """ Create a new conflict """
        conflict = Conflict(uai_number=uai_number,
                            field_name=field_name,
                            current_value=current_value,
                            new_value=new_value,
                            active=active,
                            id_esr=id_esr)
        return conflict.save()
