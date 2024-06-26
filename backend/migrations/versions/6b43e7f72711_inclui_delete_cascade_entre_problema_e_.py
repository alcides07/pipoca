"""inclui delete cascade entre problema e arquivo

Revision ID: 6b43e7f72711
Revises: 0b76d8569b3a
Create Date: 2024-03-30 14:25:43.918567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b43e7f72711'
down_revision = '0b76d8569b3a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('arquivos', schema=None) as batch_op:
        batch_op.drop_constraint('arquivos_problema_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('arquivos_problema_id_fkey', 'problemas', ['problema_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('arquivos', schema=None) as batch_op:
        batch_op.drop_constraint('arquivos_problema_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('arquivos_problema_id_fkey', 'problemas', ['problema_id'], ['id'])

    # ### end Alembic commands ###
