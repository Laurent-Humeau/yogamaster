"""Add a max number of participants and current participants

Revision ID: 9c8cdbb2d0d1
Revises: 216511edcd06
Create Date: 2024-09-18 06:05:56.513986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c8cdbb2d0d1'
down_revision = '216511edcd06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('yogacourse', schema=None) as batch_op:
        batch_op.add_column(sa.Column('max_participants', sa.Integer(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('current_participants', sa.Integer(), nullable=False, server_default='0'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('yogacourse', schema=None) as batch_op:
        batch_op.drop_column('current_participants')
        batch_op.drop_column('max_participants')

    # ### end Alembic commands ###
