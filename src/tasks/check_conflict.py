import logging
from repositories import ConflictRepository #, DatabaseBridgeRepository

def check_for_all_conflict(
    siret, business_name, address_1, address_2, zip_code, city, country, 
    city_code, naf, date_ouverture, tranche_effectif, esr_institution):
    logging.info('in Check for all conflict')
    check_for_conflict(siret=siret, sirene_field='business_name', sirene_value=business_name, esr_institution=esr_institution)
    check_for_conflict(siret=siret, sirene_field='address_1', sirene_value=address_1, esr_institution=esr_institution)
    check_for_conflict(siret=siret, sirene_field='address_2', sirene_value=address_2, esr_institution=esr_institution)
    check_for_conflict(siret=siret, sirene_field='zip_code', sirene_value=zip_code, esr_institution=esr_institution)
    check_for_conflict(siret=siret, sirene_field='city', sirene_value=city, esr_institution=esr_institution)
    check_for_conflict(siret=siret, sirene_field='country', sirene_value=country, esr_institution=esr_institution)
    check_for_conflict(siret=siret, sirene_field='city_code', sirene_value=city_code, esr_institution=esr_institution)
    check_for_conflict(siret=siret, sirene_field='naf', sirene_value=naf, esr_institution=esr_institution)
    check_for_conflict(siret=siret, sirene_field='date_ouverture', sirene_value=date_ouverture, esr_institution=esr_institution)
    check_for_conflict(siret=siret, sirene_field='tranche_effectif', sirene_value=tranche_effectif, esr_institution=esr_institution)

def check_for_conflict(siret, sirene_field, sirene_value, esr_institution):
    logging.info('In check for conflict : %s', sirene_field)
    if sirene_field == 'naf':
        logging.info('In check for conflict NAF')
    esr_value = get_esr_value(sirene_field, esr_institution)
    resource_dict = { 'business_name': 'address', 'address_1': 'address', 'address_2': 'address', 'zip_code': 'address', 'city': 'address', 'country': 'address', 'city_code': 'address', 'naf': 'code', 'date_ouverture': 'institution', 'tranche_effectif': 'institution' }
    category_dict = { 'business_name': None, 'address_1': None, 'address_2': None, 'zip_code': None, 'city': None, 'country': None, 'city_code': None, 'naf': 'naf', 'date_ouverture': None, 'tranche_effectif': None }
    if not esr_value == sirene_value:
        ConflictRepository.create(
            source_id=siret,
            source='sirene',
            resource=resource_dict[sirene_field],
            category=category_dict[sirene_field],
            field_name=sirene_field,
            current_value=esr_value,
            new_value=sirene_value,
            active=True,
            id_esr=esr_institution['id'])
        logging.info('%s: conflict created with resource: %s, category: %s, field: %s', siret, resource_dict[sirene_field], category_dict[sirene_field], sirene_field)

def get_esr_value(sirene_field, esr_institution):

    logging.info(esr_institution)
    esr_address = ''
    for address in esr_institution['addresses']: 
        if address['status'] == 'active':
            esr_address = address

    if sirene_field == 'business_name':
        return esr_address['business_name']
    if sirene_field == 'address_1':
        return esr_address['address_1']
    if sirene_field == 'address_2':
        return esr_address['address_2']
    if sirene_field == 'zip_code':
        return esr_address['zip_code']
    if sirene_field == 'city':
        return esr_address['city']
    if sirene_field == 'country':
        return esr_address['country']
    if sirene_field == 'city_code':
        return esr_address['city_code']
    if sirene_field == 'naf':
        logging.info('###### SIRENE #######')
        logging.info(sirene_field)
        for code in esr_institution['codes']:
            if code['category'] == 'naf':
                logging.info(code['content'])
                return code['content']
    if sirene_field == 'date_ouverture':
        return esr_institution['date_start']
    if sirene_field == 'tranche_effectif':
        return esr_institution['size_range']

def check_for_all_conflict_with_snapshot(
    siret, business_name, address_1, address_2, zip_code, city, country, 
    city_code, naf, date_ouverture, tranche_effectif, esr_institution, snapshot):
    """ check for conflict within snapshot and then with esr value"""

    if snapshot.business_name != business_name:
        check_for_conflict(siret=siret, sirene_field='business_name', sirene_value=business_name, esr_institution=esr_institution)

    if snapshot.address_1 != address_1:
        check_for_conflict(siret=siret, sirene_field='address_1', sirene_value=address_1, esr_institution=esr_institution)

    if snapshot.address_2 != address_2:
        check_for_conflict(siret=siret, sirene_field='address_2', sirene_value=address_2, esr_institution=esr_institution)

    if snapshot.zip_code != zip_code:
        check_for_conflict(siret=siret, sirene_field='zip_code', sirene_value=zip_code, esr_institution=esr_institution)

    if snapshot.city != city:
        check_for_conflict(siret=siret, sirene_field='city', sirene_value=city, esr_institution=esr_institution)

    if snapshot.country != country:
        check_for_conflict(siret=siret, sirene_field='country', sirene_value=country, esr_institution=esr_institution)

    if snapshot.city_code != city_code:
        check_for_conflict(siret=siret, sirene_field='city_code', sirene_value=city_code, esr_institution=esr_institution)

    if snapshot.naf != naf:
        check_for_conflict(siret=siret, sirene_field='naf', sirene_value=naf, esr_institution=esr_institution)

    if snapshot.date_ouverture != date_ouverture:
        check_for_conflict(siret=siret, sirene_field='date_ouverture', sirene_value=date_ouverture, esr_institution=esr_institution)

    if snapshot.tranche_effectif != tranche_effectif:
        check_for_conflict(siret=siret, sirene_field='tranche_effectif', sirene_value=tranche_effectif, esr_institution=esr_institution)


########## BCE ############

def check_for_bce_conflict(uai, bce_field, bce_value, esr_institution):
    esr_value = get_esr_value(bce_field, esr_institution)
    if not esr_value == bce_value:
        ConflictRepository.create(
            source_id=uai, source='bce', resource='resource', category='cat', field_name=bce_field,
            current_value=esr_value, new_value=bce_value, active=True,
            id_esr=esr_institution['id'])
        logging.info('%s: conflict created with field %s', uai, bce_field)


def check_for_all_bce_conflict(
        uai, sigle, patronyme, date_ouverture, date_fermeture,
        numero_siren_siret, adresse, boite_postale,
        code_postal, localite_acheminement, numero_telephone,
        secteur_public_prive, ministere_tutelle, categorie_juridique,
        site_web, commune, esr_institution):
        check_for_bce_conflict(
            uai=uai, bce_field='sigle_uai',
            bce_value=sigle, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='patronyme_uai',
            bce_value=patronyme, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='date_ouverture',
            bce_value=date_ouverture, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='date_fermeture',
            bce_value=date_fermeture, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='numero_siren_siret_uai',
            bce_value=numero_siren_siret, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='adresse_uai',
            bce_value=adresse, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='boite_postale_uai',
            bce_value=boite_postale, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='code_postal_uai',
            bce_value=code_postal, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='localite_acheminement_uai',
            bce_value=localite_acheminement,
            esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='numero_telephone_uai',
            bce_value=numero_telephone, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='secteur_public_prive',
            bce_value=secteur_public_prive, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='ministere_tutelle',
            bce_value=ministere_tutelle, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='categorie_juridique',
            bce_value=categorie_juridique, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='site_web',
            bce_value=site_web, esr_institution=esr_institution)
        check_for_bce_conflict(
            uai=uai, bce_field='commune',
            bce_value=commune, esr_institution=esr_institution)


def check_for_all_bce_conflict_with_snapshot(
        uai, sigle, patronyme, date_ouverture, date_fermeture,
        numero_siren_siret, adresse, boite_postale,
        code_postal, localite_acheminement, numero_telephone,
        secteur_public_prive, ministere_tutelle, categorie_juridique,
        site_web, commune, esr_institution, snapshot):
        """ check for conflict within snapshot and then with esr value"""

        if snapshot.sigle != sigle:
            check_for_bce_conflict(
                uai=uai, bce_field='sigle_uai',
                bce_value=sigle_uai, esr_institution=esr_institution)

        if snapshot.patronyme != patronyme:
            check_for_bce_conflict(
                uai=uai, bce_field='patronyme_uai',
                bce_value=patronyme_uai, esr_institution=esr_institution)

        if snapshot.date_ouverture != date_ouverture:
            check_for_bce_conflict(
                uai=uai, bce_field='date_ouverture',
                bce_value=date_ouverture, esr_institution=esr_institution)

        if snapshot.date_fermeture != date_fermeture:
            check_for_bce_conflict(
                uai=uai, bce_field='date_fermeture',
                bce_value=date_fermeture, esr_institution=esr_institution)

        if snapshot.numero_siren_siret != numero_siren_siret:
            check_for_bce_conflict(
                uai=uai, bce_field='numero_siren_siret_uai',
                bce_value=numero_siren_siret_uai,
                esr_institution=esr_institution)

        if snapshot.adresse != adresse:
            check_for_bce_conflict(
                uai=uai, bce_field='adresse_uai',
                bce_value=adresse_uai, esr_institution=esr_institution)

        if snapshot.boite_postale != boite_postale:
            check_for_bce_conflict(
                uai=uai, bce_field='boite_postale_uai',
                bce_value=boite_postale_uai, esr_institution=esr_institution)

        if snapshot.code_postal != code_postal:
            check_for_bce_conflict(
                uai=uai, bce_field='code_postal_uai',
                bce_value=code_postal_uai, esr_institution=esr_institution)

        if (snapshot.localite_acheminement !=
                localite_acheminement):
            check_for_bce_conflict(
                uai=uai, bce_field='localite_acheminement_uai',
                bce_value=localite_acheminement_uai,
                esr_institution=esr_institution)

        if snapshot.numero_telephone != numero_telephone:
            check_for_bce_conflict(
                uai=uai, bce_field='numero_telephone_uai',
                bce_value=numero_telephone_uai,
                esr_institution=esr_institution)

        if snapshot.secteur_public_prive != secteur_public_prive:
            check_for_bce_conflict(
                uai=uai, bce_field='secteur_public_prive',
                bce_value=secteur_public_prive,
                esr_institution=esr_institution)

        if snapshot.ministere_tutelle != ministere_tutelle:
            check_for_bce_conflict(
                uai=uai, bce_field='ministere_tutelle',
                bce_value=ministere_tutelle, esr_institution=esr_institution)

        if snapshot.categorie_juridique != categorie_juridique:
            check_for_bce_conflict(
                uai=uai, bce_field='categorie_juridique',
                bce_value=categorie_juridique, esr_institution=esr_institution)

        if snapshot.site_web != site_web:
            check_for_bce_conflict(
                uai=uai, bce_field='site_web',
                bce_value=site_web, esr_institution=esr_institution)

        if snapshot.commune != commune:
            check_for_bce_conflict(
                uai=uai, bce_field='commune',
                bce_value=commune, esr_institution=esr_institution)

