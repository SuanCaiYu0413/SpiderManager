"""empty message

Revision ID: d64ebd9e94c5
Revises: 20187deb9dcd
Create Date: 2018-04-25 16:47:53.050804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd64ebd9e94c5'
down_revision = '20187deb9dcd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('host_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('host_name', sa.String(length=50), nullable=False),
    sa.Column('ip_address', sa.String(length=50), nullable=False),
    sa.Column('port_num', sa.String(length=50), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('host_list')
    # ### end Alembic commands ###
