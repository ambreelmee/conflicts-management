"""Create the Institution table

Revision ID: 4105ba726b
Revises: 4f2e2c180af
Create Date: 2018-05-15 14:46:04.990652

"""

# revision identifiers, used by Alembic.
revision = '4105ba726b'
down_revision = '4f2e2c180af'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'institution',
        sa.Column('uai_number', sa.String(length=20), nullable=False),
        sa.Column('is_institution', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('uai_number')
    )


def downgrade():
    op.drop_table('institution')
