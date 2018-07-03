""" Defines the Conflict repository """

from models import Conflict


class ConflictRepository:
    """ The repository for the conflict model """

    @staticmethod
    def get(id):
        """ Query a conflict with its id """
        print('get alone')
        return Conflict.query.filter_by(
            id=id,
        ).one()

    @staticmethod
    def getConflictsByInstitution(id_esr):
        """ Query all conflicts for a given institution """
        return Conflict.query.filter_by(
            id_esr=id_esr,
        ).all()

    def getAllConflicts():
        return Conflict.query.all()

    def update(self, id, active):
        """ Update a conflict's status"""
        conflict = self.get(id)
        conflict.active = active
        return conflict.save()

    @staticmethod
    def create(source_id,
               source,
               resource,
               category, 
               field_name,
               current_value,
               new_value,
               active,
               id_esr):
        """ Create a new conflict """
        conflict = Conflict(source_id=source_id,
                            source=source,
                            resource=resource,
                            category=category,
                            field_name=field_name,
                            current_value=current_value,
                            new_value=new_value,
                            active=active,
                            id_esr=id_esr)
        return conflict.save()

