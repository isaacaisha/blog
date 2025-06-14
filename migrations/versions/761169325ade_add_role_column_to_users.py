"""Add role column to users

Revision ID: 761169325ade
Revises: 
Create Date: 2025-05-01 03:45:23.813030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '761169325ade'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=19), nullable=False, server_default='user'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
