"""Create Conflict tables

Revision ID: 22bfcbf04e9
Revises: None
Create Date: 2018-07-09 12:28:35.394036

"""

# revision identifiers, used by Alembic.
revision = '22bfcbf04e9'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('bce_institution',
    sa.Column('uai', sa.String(length=20), nullable=False),
    sa.Column('is_institution', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('uai')
    )
    op.create_table('conflict',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.String(length=20), nullable=False),
    sa.Column('source', sa.String(length=20), nullable=False),
    sa.Column('resource', sa.String(length=50), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('field_name', sa.String(length=50), nullable=False),
    sa.Column('current_value', sa.String(length=120), nullable=True),
    sa.Column('new_value', sa.String(length=120), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('id_esr', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('database_bridge',
    sa.Column('source_field', sa.String(length=30), nullable=False),
    sa.Column('bloc', sa.String(length=30), nullable=True),
    sa.Column('value_key', sa.String(length=30), nullable=False),
    sa.Column('criterion_key', sa.String(length=30), nullable=True),
    sa.Column('criterion_value', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('source_field')
    )
    op.create_table('bce_snapshot',
    sa.Column('uai', sa.String(length=8), nullable=False),
    sa.Column('sigle', sa.String(length=14), nullable=True),
    sa.Column('patronyme', sa.String(length=30), nullable=True),
    sa.Column('date_ouverture', sa.DateTime(), nullable=True),
    sa.Column('date_fermeture', sa.DateTime(), nullable=True),
    sa.Column('numero_siren_siret', sa.String(length=14), nullable=True),
    sa.Column('adresse', sa.String(length=32), nullable=True),
    sa.Column('boite_postale', sa.String(length=7), nullable=True),
    sa.Column('code_postal', sa.String(length=5), nullable=True),
    sa.Column('localite_acheminement', sa.String(length=32), nullable=True),
    sa.Column('numero_telephone', sa.String(length=13), nullable=True),
    sa.Column('secteur_public_prive', sa.String(length=2), nullable=True),
    sa.Column('ministere_tutelle', sa.String(length=2), nullable=True),
    sa.Column('categorie_juridique', sa.String(length=3), nullable=True),
    sa.Column('site_web', sa.String(length=100), nullable=True),
    sa.Column('commune', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('uai')
    )
    op.create_table('sirene_institution',
    sa.Column('siret', sa.String(length=20), nullable=False),
    sa.Column('date_maj', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('siret')
    )
    op.create_table('sirene_snapshot',
    sa.Column('siret', sa.String(length=20), nullable=False),
    sa.Column('business_name', sa.String(length=40), nullable=True),
    sa.Column('address_1', sa.String(length=40), nullable=True),
    sa.Column('address_2', sa.String(length=40), nullable=True),
    sa.Column('zip_code', sa.String(length=5), nullable=True),
    sa.Column('city', sa.String(length=40), nullable=True),
    sa.Column('country', sa.String(length=40), nullable=True),
    sa.Column('city_code', sa.String(length=20), nullable=True),
    sa.Column('naf', sa.String(length=5), nullable=True),
    sa.Column('date_ouverture', sa.DateTime(), nullable=True),
    sa.Column('tranche_effectif', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('siret')
    )


def downgrade():
    op.drop_table('sirene_snapshot')
    op.drop_table('sirene_institution')
    op.drop_table('bce_snapshot')
    op.drop_table('database_bridge')
    op.drop_table('conflict')
    op.drop_table('bce_institution')
