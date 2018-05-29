""" Defines the InstitutionSnapshot repository """

from models import DatabaseConnection


class DatabaseConnectionRepository:
    """ The repository for the DatabaseConnection model """

    @staticmethod
    def get(bce_field):
        """ Query a connection's snapshot by its id """
        return DatabaseConnection.query.filter_by(
            bce_field=bce_field,
        ).first()
