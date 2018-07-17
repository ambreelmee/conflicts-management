""" Defines the DatabaseBridge repository """

from models import DatabaseBridge


class DatabaseBridgeRepository:
    """ The repository for the DatabaseBridge model """

    @staticmethod
    def get(source_field):
        """ Query a connection's snapshot by its id """
        return DatabaseBridge.query.filter_by(
            source_field=source_field,
        ).first()

    def create(source_field, bloc, value_key, criterion_key, criterion_value):
        """ Create a new database bridge """
        bridge = DatabaseBridge(
            source_field=source_field,
            bloc=bloc,
            value_key=value_key,
            criterion_key=criterion_key,
            criterion_value=criterion_value)

        return bridge.save()
