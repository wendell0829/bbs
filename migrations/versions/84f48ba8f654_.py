"""empty message

Revision ID: 84f48ba8f654
Revises: 9ab7bac13d97
Create Date: 2019-03-16 11:12:19.045970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84f48ba8f654'
down_revision = '9ab7bac13d97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('creat_time', sa.DateTime(), nullable=True),
    sa.Column('cms_user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cms_user_id'], ['cms_user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('creat_time', sa.DateTime(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.String(length=25), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['front_user.id'], ),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('board')
    # ### end Alembic commands ###
