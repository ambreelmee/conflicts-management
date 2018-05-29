"""Create database_connection Table

Revision ID: 4431bb8497a
Revises: 168a2ff40b3
Create Date: 2018-05-29 14:41:17.547929

"""

# revision identifiers, used by Alembic.
revision = '4431bb8497a'
down_revision = '168a2ff40b3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('database_connection',
    sa.Column('bce_field', sa.String(length=30), nullable=False),
    sa.Column('bloc', sa.String(length=30), nullable=True),
    sa.Column('value_key', sa.String(length=30), nullable=False),
    sa.Column('criterion_key', sa.String(length=30), nullable=True),
    sa.Column('criterion_value', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('bce_field')
    )


def downgrade():
    op.drop_table('database_connection')
