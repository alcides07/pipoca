"""inclui delete CASCADE entre problema e testes

Revision ID: c4ad22aed76f
Revises: b54012cc8c39
Create Date: 2024-03-30 14:29:56.126474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4ad22aed76f'
down_revision = 'b54012cc8c39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('problema_testes', schema=None) as batch_op:
        batch_op.drop_constraint('problema_testes_problema_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('problema_testes_problema_id_fkey', 'problemas', ['problema_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('problema_testes', schema=None) as batch_op:
        batch_op.drop_constraint('problema_testes_problema_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('problema_testes_problema_id_fkey', 'problemas', ['problema_id'], ['id'])

    # ### end Alembic commands ###
