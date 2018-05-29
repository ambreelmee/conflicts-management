"""Create Institution_snapshot table

Revision ID: 17458089ba6
Revises: 47c5f58fe5e
Create Date: 2018-05-17 14:35:43.321289

"""

# revision identifiers, used by Alembic.
revision = '17458089ba6'
down_revision = '47c5f58fe5e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'institution_snapshot',
        sa.Column('numero_uai', sa.String(length=8), nullable=False),
        sa.Column('sigle_uai', sa.String(length=14), nullable=True),
        sa.Column('patronyme_uai', sa.String(length=30), nullable=True),
        sa.Column('date_ouverture', sa.DateTime(), nullable=True),
        sa.Column('date_fermeture', sa.DateTime(), nullable=True),
        sa.Column(
            'numero_siren_siret_uai', sa.String(length=14), nullable=True),
        sa.Column('adresse_uai', sa.String(length=32), nullable=True),
        sa.Column('boite_postale_uai', sa.String(length=7), nullable=True),
        sa.Column('code_postal_uai', sa.String(length=5), nullable=True),
        sa.Column(
            'localite_acheminement_uai', sa.String(length=32), nullable=True),
        sa.Column('numero_telephone_uai', sa.String(length=13), nullable=True),
        sa.Column('secteur_public_prive', sa.String(length=2), nullable=True),
        sa.Column('ministere_tutelle', sa.String(length=2), nullable=True),
        sa.Column('categorie_juridique', sa.String(length=3), nullable=True),
        sa.Column('site_web', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('numero_uai')
    )


def downgrade():
    op.drop_table('institution_snapshot')
