"""empty message

Revision ID: ed8bf86fcc46
Revises: c31a2a7294ea
Create Date: 2022-10-14 21:43:42.305471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed8bf86fcc46'
down_revision = 'c31a2a7294ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('sqlite_sequence')
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###
