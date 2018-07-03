from repositories import DatabaseBridgeRepository


def seed_database_bridge():
    DatabaseBridgeRepository.create('sigle_uai', 'name', 'initials', None, None)
    DatabaseBridgeRepository.create('patronyme_uai', 'name', 'text', None, None)
    DatabaseBridgeRepository.create('date_ouverture', None, 'date_start', None, None)
    DatabaseBridgeRepository.create('date_fermeture', None, 'date_end', None, None)
    DatabaseBridgeRepository.create('numero_siren_siret_uai', 'codes', 'content', 'category', 'siret')
    DatabaseBridgeRepository.create('adresse_uai', 'address', 'address_1', None, None)
    DatabaseBridgeRepository.create('boite_postale_uai', 'address', 'address_2', None, None)
    DatabaseBridgeRepository.create('code_postal_uai', 'address', 'zip_code', None, None)
    DatabaseBridgeRepository.create('localite_acheminement_uai', 'address', 'city', None, None)
    DatabaseBridgeRepository.create('numero_telephone_uai', 'address', 'phone', None, None)
    DatabaseBridgeRepository.create('commune', 'address', 'city_code', None, None)
    DatabaseBridgeRepository.create('secteur_public_prive', 'tags', 'id', 'category', 'secteur public prive')
    DatabaseBridgeRepository.create('ministere_tutelle', 'tags', 'id', 'category', 'ministere tutelle')
    DatabaseBridgeRepository.create('categorie_juridique', 'tags', 'id', 'category', 'catégorie juridique')
    DatabaseBridgeRepository.create('site_web', 'links', 'content', 'category', 'website')
    DatabaseBridgeRepository.create('numero_uai', 'codes', 'content', 'category', 'uai')
