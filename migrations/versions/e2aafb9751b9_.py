"""empty message

Revision ID: e2aafb9751b9
Revises: fbe143775742
Create Date: 2020-08-28 14:39:29.112077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2aafb9751b9'
down_revision = 'fbe143775742'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uid', 'fid')
    )
    op.add_column('user', sa.Column('n_fan', sa.Integer(), nullable=False))
    op.add_column('user', sa.Column('n_follow', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'n_follow')
    op.drop_column('user', 'n_fan')
    op.drop_table('follow')
    # ### end Alembic commands ###
