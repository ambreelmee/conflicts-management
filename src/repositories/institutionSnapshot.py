""" Defines the InstitutionSnapshot repository """

from models import InstitutionSnapshot


class InstitutionSnapshotRepository:
    """ The repository for the institutionSnapshot model """

    @staticmethod
    def get(numero_uai):
        """ Query an insitution's snapshot by its uai_number """
        return InstitutionSnapshot.query.filter_by(
            numero_uai=numero_uai,
        ).first()

    def update(self,
               numero_uai,
               sigle_uai=None,
               patronyme_uai=None,
               date_ouverture=None,
               date_fermeture=None,
               numero_siren_siret_uai=None,
               adresse_uai=None,
               boite_postale_uai=None,
               code_postal_uai=None,
               localite_acheminement_uai=None,
               numero_telephone_uai=None,
               secteur_public_prive=None,
               ministere_tutelle=None,
               categorie_juridique=None,
               site_web=None):
        """ Update an institution's snapshot """
        institution = self.get(numero_uai)
        if sigle_uai:
            institution.sigle_uai = sigle_uai
        if patronyme_uai:
            institution.patronyme_uai = patronyme_uai
        if date_ouverture:
            institution.date_ouverture = date_ouverture
        if date_fermeture:
            institution.date_fermeture = date_fermeture
        if numero_siren_siret_uai:
            institution.numero_siren_siret_uai = numero_siren_siret_uai
        if adresse_uai:
            institution.adresse_uai = adresse_uai
        if boite_postale_uai:
            institution.boite_postale_uai = boite_postale_uai
        if code_postal_uai:
            institution.code_postal_uai = code_postal_uai
        if localite_acheminement_uai:
            institution.localite_acheminement_uai = localite_acheminement_uai
        if numero_telephone_uai:
            institution.numero_telephone_uai = numero_telephone_uai
        if secteur_public_prive:
            institution.secteur_public_prive = secteur_public_prive
        if ministere_tutelle:
            institution.ministere_tutelle = ministere_tutelle
        if categorie_juridique:
            institution.categorie_juridique = categorie_juridique
        if site_web:
            institution.site_web = site_web

        return institution.save()

    @staticmethod
    def create(numero_uai,
               sigle_uai=None,
               patronyme_uai=None,
               date_ouverture=None,
               date_fermeture=None,
               numero_siren_siret_uai=None,
               adresse_uai=None,
               boite_postale_uai=None,
               code_postal_uai=None,
               localite_acheminement_uai=None,
               numero_telephone_uai=None,
               secteur_public_prive=None,
               ministere_tutelle=None,
               categorie_juridique=None,
               site_web=None):
        """ Create a new institution snapshot """
        institution = InstitutionSnapshot(
            numero_uai=numero_uai,
            sigle_uai=sigle_uai,
            patronyme_uai=patronyme_uai,
            date_ouverture=date_ouverture,
            date_fermeture=date_fermeture,
            numero_siren_siret_uai=numero_siren_siret_uai,
            adresse_uai=adresse_uai,
            boite_postale_uai=boite_postale_uai,
            code_postal_uai=code_postal_uai,
            localite_acheminement_uai=localite_acheminement_uai,
            numero_telephone_uai=numero_telephone_uai,
            secteur_public_prive=secteur_public_prive,
            ministere_tutelle=ministere_tutelle,
            categorie_juridique=categorie_juridique,
            site_web=site_web)

        return institution.save()
