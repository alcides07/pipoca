"""inclui delete SET NULL entre problema e resposta

Revision ID: 2d302608bc4b
Revises: 5534a923cf14
Create Date: 2024-03-30 14:28:09.802195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d302608bc4b'
down_revision = '5534a923cf14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('problema_respostas', schema=None) as batch_op:
        batch_op.drop_constraint('problema_respostas_problema_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('problema_respostas_problema_id_fkey', 'problemas', ['problema_id'], ['id'], ondelete='SET NULL')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('problema_respostas', schema=None) as batch_op:
        batch_op.drop_constraint('problema_respostas_problema_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('problema_respostas_problema_id_fkey', 'problemas', ['problema_id'], ['id'])

    # ### end Alembic commands ###
