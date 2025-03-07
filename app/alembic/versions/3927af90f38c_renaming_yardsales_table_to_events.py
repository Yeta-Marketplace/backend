"""Renaming yardsales table to events

Revision ID: 3927af90f38c
Revises: 15956e35ee96
Create Date: 2022-11-29 03:36:24.337684

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3927af90f38c'
down_revision = '15956e35ee96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('yardsale', 'event')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('event', 'yardsale')
    # ### end Alembic commands ###
