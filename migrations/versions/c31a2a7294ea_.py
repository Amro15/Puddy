"""put back curr line breaks null

Revision ID: c31a2a7294ea
Revises: c2191574b635
Create Date: 2022-10-14 21:42:59.533564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c31a2a7294ea'
down_revision = 'c2191574b635'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('sqlite_sequence')
    with op.batch_alter_table('current_unsaved_poem', schema=None) as batch_op:
        batch_op.alter_column('current_line_breaks',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('current_unsaved_poem', schema=None) as batch_op:
        batch_op.alter_column('current_line_breaks',
               existing_type=sa.INTEGER(),
               nullable=True)

    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###
