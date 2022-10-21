"""Add created_on to User and YardSale

Revision ID: e2c3937c6879
Revises: ab711e95da32
Create Date: 2022-10-21 03:37:40.413884

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'e2c3937c6879'
down_revision = 'ab711e95da32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('created_on', sa.DateTime(), nullable=False, server_default='NOW()'))
    op.add_column('yardsale', sa.Column('created_on', sa.DateTime(), nullable=False, server_default='NOW()'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('yardsale', 'created_on')
    op.drop_column('user', 'created_on')
    # ### end Alembic commands ###
