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

    def create(bce_field, bloc, value_key, criterion_key, criterion_value):
        """ Create a new database connection """
        connection = DatabaseConnection(
            bce_field=bce_field,
            bloc=bloc,
            value_key=value_key,
            criterion_key=criterion_key,
            criterion_value=criterion_value)

        return connection.save()
