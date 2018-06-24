"""empty message

Revision ID: 56904b093758
Revises: 
Create Date: 2018-06-14 18:14:53.839941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56904b093758'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('ip', sa.VARCHAR(length=50), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('user', sa.VARCHAR(length=50), nullable=True),
    sa.Column('pwd', sa.VARCHAR(length=50), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), nullable=False),
    sa.Column('_password', sa.VARCHAR(length=320), nullable=False),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('clients')
    # ### end Alembic commands ###