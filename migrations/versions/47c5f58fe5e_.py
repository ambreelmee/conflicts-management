"""Create the conflict table

Revision ID: 47c5f58fe5e
Revises: 4105ba726b
Create Date: 2018-05-17 11:57:23.912080

"""

# revision identifiers, used by Alembic.
revision = '47c5f58fe5e'
down_revision = '4105ba726b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'conflict',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uai_number', sa.String(length=20), nullable=False),
        sa.Column('field_name', sa.String(length=50), nullable=False),
        sa.Column('current_value', sa.String(length=120), nullable=True),
        sa.Column('new_value', sa.String(length=120), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('id_esr', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('conflict')
