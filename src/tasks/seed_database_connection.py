from repositories import DatabaseConnectionRepository


def seed_database_connection():
    DatabaseConnectionRepository.create(
        'sigle_uai', 'name', 'initials', None, None)
    DatabaseConnectionRepository.create(
        'patronyme_uai', 'name', 'text', None, None)
    DatabaseConnectionRepository.create(
        'date_ouverture', None, 'date_start', None, None)
    DatabaseConnectionRepository.create(
        'date_fermeture', None, 'date_end', None, None)
    DatabaseConnectionRepository.create(
        'numero_siren_siret_uai', 'codes', 'content', 'category', 'siret')
    DatabaseConnectionRepository.create(
        'adresse_uai', 'address', 'address_1', None, None)
    DatabaseConnectionRepository.create(
        'boite_postale_uai', 'address', 'address_2', None, None)
    DatabaseConnectionRepository.create(
        'code_postal_uai', 'address', 'zip_code', None, None)
    DatabaseConnectionRepository.create(
        'localite_acheminement_uai', 'address', 'city', None, None)
    DatabaseConnectionRepository.create(
        'numero_telephone_uai', 'address', 'phone', None, None)
    DatabaseConnectionRepository.create(
        'secteur_public_prive', 'tags', 'id', 'category',
        'secteur public prive')
    DatabaseConnectionRepository.create(
        'ministere_tutelle', 'tags', 'id', 'category', 'ministere tutelle')
    DatabaseConnectionRepository.create(
        'categorie_juridique', 'tags', 'id', 'category', 'catégorie juridique')
    DatabaseConnectionRepository.create(
        'site_web', 'links', 'content', 'category', 'website')
    DatabaseConnectionRepository.create(
        'numero_uai', 'codes', 'content', 'category', 'uai')
