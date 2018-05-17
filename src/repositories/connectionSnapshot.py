""" Defines the InstitutionSnapshot repository """

from models import ConnectionSnapshot


class ConnectionSnapshotRepository:
    """ The repository for the ConnectionSnapshot model """

    @staticmethod
    def get(id):
        """ Query a connection's snapshot by its id """
        return ConnectionSnapshot.query.filter_by(
            id=id,
        ).one()

    @staticmethod
    def getAllConnectionsByInstitution(numero_uai):
        """ Query all connections for a given institution """
        return ConnectionSnapshot.query.filter_by(
            numero_uai=numero_uai,
        ).all()

    def update(self,
               id,
               numero_uai=None,
               numero_uai_rattachee=None,
               type_rattachement=None,
               date_ouverture=None,
               date_fermeture=None):
        """ Update a connection's snapshot """
        connection = self.get(id)
        if numero_uai:
            connection.numero_uai = numero_uai
        if numero_uai_rattachee:
            connection.numero_uai_rattachee = numero_uai_rattachee
        if type_rattachement:
            connection.type_rattachement = type_rattachement
        if date_ouverture:
            connection.date_ouverture = date_ouverture
        if date_fermeture:
            connection.date_fermeture = date_fermeture

        return connection.save()

    @staticmethod
    def create(numero_uai,
               numero_uai_rattachee=None,
               type_rattachement=None,
               date_ouverture=None,
               date_fermeture=None):
        """ Create a new connection snapshot """
        connection = ConnectionSnapshot(
            numero_uai=numero_uai,
            numero_uai_rattachee=numero_uai_rattachee,
            type_rattachement=type_rattachement,
            date_ouverture=date_ouverture,
            date_fermeture=date_fermeture)

        return connection.save()
