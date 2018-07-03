""" Defines the BceSnapshot repository """

from models import BceSnapshot


class BceSnapshotRepository:
    """ The repository for the BceSnapshot model """

    @staticmethod
    def get(uai):
        """ Query an insitution's snapshot by its uai """
        return BceSnapshot.query.filter_by(uai=uai).first()

    def update(self,
               uai,
               sigle=None,
               patronyme=None,
               date_ouverture=None,
               date_fermeture=None,
               numero_siren_siret=None,
               adresse=None,
               boite_postale=None,
               code_postal=None,
               localite_acheminement=None,
               numero_telephone=None,
               secteur_public_prive=None,
               ministere_tutelle=None,
               categorie_juridique=None,
               site_web=None,
               commune=None):
        """ Update an institution's snapshot """
        institution = self.get(uai)
        if sigle:
            institution.sigle = sigle
        if patronyme:
            institution.patronyme = patronyme
        if date_ouverture:
            institution.date_ouverture = date_ouverture
        if date_fermeture:
            institution.date_fermeture = date_fermeture
        if numero_siren_siret:
            institution.numero_siren_siret = numero_siren_siret
        if adresse:
            institution.adresse = adresse
        if boite_postale:
            institution.boite_postale = boite_postale
        if code_postal:
            institution.code_postal = code_postal
        if localite_acheminement:
            institution.localite_acheminement = localite_acheminement
        if numero_telephone:
            institution.numero_telephone = numero_telephone
        if secteur_public_prive:
            institution.secteur_public_prive = secteur_public_prive
        if ministere_tutelle:
            institution.ministere_tutelle = ministere_tutelle
        if categorie_juridique:
            institution.categorie_juridique = categorie_juridique
        if site_web:
            institution.site_web = site_web
        if commune:
            institution.commune = commune

        return institution.save()

    @staticmethod
    def create(uai,
               sigle=None,
               patronyme=None,
               date_ouverture=None,
               date_fermeture=None,
               numero_siren_siret=None,
               adresse=None,
               boite_postale=None,
               code_postal=None,
               localite_acheminement=None,
               numero_telephone=None,
               secteur_public_prive=None,
               ministere_tutelle=None,
               categorie_juridique=None,
               site_web=None,
               commune=None):
        """ Create a new institution snapshot """
        institution = BceSnapshot(
            uai=uai,
            sigle=sigle,
            patronyme=patronyme,
            date_ouverture=date_ouverture,
            date_fermeture=date_fermeture,
            numero_siren_siret=numero_siren_siret,
            adresse=adresse,
            boite_postale=boite_postale,
            code_postal=code_postal,
            localite_acheminement=localite_acheminement,
            numero_telephone=numero_telephone,
            secteur_public_prive=secteur_public_prive,
            ministere_tutelle=ministere_tutelle,
            categorie_juridique=categorie_juridique,
            site_web=site_web,
            commune=commune)

        return institution.save()