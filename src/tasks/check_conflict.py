import logging
from repositories import ConflictRepository, DatabaseConnectionRepository


def get_esr_value(bce_field, esr_institution):
    connections = DatabaseConnectionRepository.get(bce_field=bce_field)
    if not connections.criterion_key:
        if connections.bloc:
            bloc = esr_institution[connections.bloc]
            if bloc:
                return bloc[connections.value_key]
            return None
        return esr_institution[connections.value_key]

    # if there is any criterion, it is always inside a bloc list
    bloc = esr_institution[connections.bloc]
    # we search for the item which match criteria
    return next((item[connections.value_key] for item in bloc
                if (item[connections.criterion_key] ==
                    connections.criterion_value)), None)


def check_for_conflict(uai_number, bce_field, bce_value, esr_institution):
    esr_value = get_esr_value(bce_field, esr_institution)
    if not esr_value == bce_value:
        ConflictRepository.create(
            uai_number=uai_number, field_name=bce_field,
            current_value=esr_value, new_value=bce_value, active=True,
            id_esr=esr_institution['id'])
        logging.info('%s: conflict created with field %s',
                     uai_number, bce_field)


def check_for_all_conflict(
        numero_uai, sigle_uai, patronyme_uai, date_ouverture, date_fermeture,
        numero_siren_siret_uai, adresse_uai, boite_postale_uai,
        code_postal_uai, localite_acheminement_uai, numero_telephone_uai,
        secteur_public_prive, ministere_tutelle, categorie_juridique,
        site_web, commune, esr_institution):
        check_for_conflict(
            uai_number=numero_uai, bce_field='sigle_uai',
            bce_value=sigle_uai, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='patronyme_uai',
            bce_value=patronyme_uai, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='date_ouverture',
            bce_value=date_ouverture, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='date_fermeture',
            bce_value=date_fermeture, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='numero_siren_siret_uai',
            bce_value=numero_siren_siret_uai, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='adresse_uai',
            bce_value=adresse_uai, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='boite_postale_uai',
            bce_value=boite_postale_uai, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='code_postal_uai',
            bce_value=code_postal_uai, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='localite_acheminement_uai',
            bce_value=localite_acheminement_uai,
            esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='numero_telephone_uai',
            bce_value=numero_telephone_uai, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='secteur_public_prive',
            bce_value=secteur_public_prive, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='ministere_tutelle',
            bce_value=ministere_tutelle, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='categorie_juridique',
            bce_value=categorie_juridique, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='site_web',
            bce_value=site_web, esr_institution=esr_institution)
        check_for_conflict(
            uai_number=numero_uai, bce_field='commune',
            bce_value=commune, esr_institution=esr_institution)


def check_for_all_conflict_with_snapshot(
        numero_uai, sigle_uai, patronyme_uai, date_ouverture, date_fermeture,
        numero_siren_siret_uai, adresse_uai, boite_postale_uai,
        code_postal_uai, localite_acheminement_uai, numero_telephone_uai,
        secteur_public_prive, ministere_tutelle, categorie_juridique,
        site_web, commune, esr_institution, snapshot):
        """ check for conflict within snapshot and then with esr value"""

        if snapshot.sigle_uai != sigle_uai:
            check_for_conflict(
                uai_number=numero_uai, bce_field='sigle_uai',
                bce_value=sigle_uai, esr_institution=esr_institution)

        if snapshot.patronyme_uai != patronyme_uai:
            check_for_conflict(
                uai_number=numero_uai, bce_field='patronyme_uai',
                bce_value=patronyme_uai, esr_institution=esr_institution)

        if snapshot.date_ouverture != date_ouverture:
            check_for_conflict(
                uai_number=numero_uai, bce_field='date_ouverture',
                bce_value=date_ouverture, esr_institution=esr_institution)

        if snapshot.date_fermeture != date_fermeture:
            check_for_conflict(
                uai_number=numero_uai, bce_field='date_fermeture',
                bce_value=date_fermeture, esr_institution=esr_institution)

        if snapshot.numero_siren_siret_uai != numero_siren_siret_uai:
            check_for_conflict(
                uai_number=numero_uai, bce_field='numero_siren_siret_uai',
                bce_value=numero_siren_siret_uai,
                esr_institution=esr_institution)

        if snapshot.adresse_uai != adresse_uai:
            check_for_conflict(
                uai_number=numero_uai, bce_field='adresse_uai',
                bce_value=adresse_uai, esr_institution=esr_institution)

        if snapshot.boite_postale_uai != boite_postale_uai:
            check_for_conflict(
                uai_number=numero_uai, bce_field='boite_postale_uai',
                bce_value=boite_postale_uai, esr_institution=esr_institution)

        if snapshot.code_postal_uai != code_postal_uai:
            check_for_conflict(
                uai_number=numero_uai, bce_field='code_postal_uai',
                bce_value=code_postal_uai, esr_institution=esr_institution)

        if (snapshot.localite_acheminement_uai !=
                localite_acheminement_uai):
            check_for_conflict(
                uai_number=numero_uai, bce_field='localite_acheminement_uai',
                bce_value=localite_acheminement_uai,
                esr_institution=esr_institution)

        if snapshot.numero_telephone_uai != numero_telephone_uai:
            check_for_conflict(
                uai_number=numero_uai, bce_field='numero_telephone_uai',
                bce_value=numero_telephone_uai,
                esr_institution=esr_institution)

        if snapshot.secteur_public_prive != secteur_public_prive:
            check_for_conflict(
                uai_number=numero_uai, bce_field='secteur_public_prive',
                bce_value=secteur_public_prive,
                esr_institution=esr_institution)

        if snapshot.ministere_tutelle != ministere_tutelle:
            check_for_conflict(
                uai_number=numero_uai, bce_field='ministere_tutelle',
                bce_value=ministere_tutelle, esr_institution=esr_institution)

        if snapshot.categorie_juridique != categorie_juridique:
            check_for_conflict(
                uai_number=numero_uai, bce_field='categorie_juridique',
                bce_value=categorie_juridique, esr_institution=esr_institution)

        if snapshot.site_web != site_web:
            check_for_conflict(
                uai_number=numero_uai, bce_field='site_web',
                bce_value=site_web, esr_institution=esr_institution)

        if snapshot.commune != commune:
            check_for_conflict(
                uai_number=numero_uai, bce_field='commune',
                bce_value=commune, esr_institution=esr_institution)
