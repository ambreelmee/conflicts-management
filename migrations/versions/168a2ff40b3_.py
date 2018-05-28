"""Create Connection_snapshot table

Revision ID: 168a2ff40b3
Revises: 17458089ba6
Create Date: 2018-05-17 15:46:49.500107

"""

# revision identifiers, used by Alembic.
revision = '168a2ff40b3'
down_revision = '17458089ba6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'connection_snapshot',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('numero_uai', sa.String(length=8), nullable=True),
        sa.Column('numero_uai_rattachee', sa.String(length=8), nullable=True),
        sa.Column('type_rattachement', sa.String(length=2), nullable=True),
        sa.Column('date_ouverture', sa.DateTime(), nullable=True),
        sa.Column('date_fermeture', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('connectionSnapshot')
