""" Defines the DatabaseBridge repository """

from models import DatabaseBridge


class DatabaseBridgeRepository:
    """ The repository for the DatabaseBridge model """

    @staticmethod
    def get(sirene_field):
        """ Query a connection's snapshot by its id """
        return DatabaseBridge.query.filter_by(
            sirene_field=sirene_field,
        ).first()

    def create(sirene_field, bloc, value_key, criterion_key, criterion_value):
        """ Create a new database bridge """
        bridge = DatabaseBridge(
            sirene_field=sirene_field,
            bloc=bloc,
            value_key=value_key,
            criterion_key=criterion_key,
            criterion_value=criterion_value)

        return bridge.save()
