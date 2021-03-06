"""empty message

Revision ID: 1d1b89033255
Revises: 84f48ba8f654
Create Date: 2019-03-16 15:03:53.775870

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1d1b89033255'
down_revision = '84f48ba8f654'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('create_time', sa.DateTime(), nullable=True))
    op.drop_column('board', 'creat_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('creat_time', mysql.DATETIME(), nullable=True))
    op.drop_column('board', 'create_time')
    # ### end Alembic commands ###
