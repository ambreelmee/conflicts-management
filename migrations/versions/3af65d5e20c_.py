"""Add commune field

Revision ID: 3af65d5e20c
Revises: 4431bb8497a
Create Date: 2018-06-22 13:59:35.264522

"""

# revision identifiers, used by Alembic.
revision = '3af65d5e20c'
down_revision = '4431bb8497a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'institution_snapshot',
        sa.Column('commune', sa.String(length=5), nullable=True))


def downgrade():
    op.drop_column('institution_snapshot', 'commune')
