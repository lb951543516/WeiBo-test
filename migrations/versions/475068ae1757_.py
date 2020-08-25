"""empty message

Revision ID: 475068ae1757
Revises: 1902e0947815
Create Date: 2020-08-25 14:08:28.349726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '475068ae1757'
down_revision = '1902e0947815'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('birthday', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'birthday')
    # ### end Alembic commands ###
