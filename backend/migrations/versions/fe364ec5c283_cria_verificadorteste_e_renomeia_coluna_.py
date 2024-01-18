"""cria verificadorTeste e renomeia coluna codigo

Revision ID: fe364ec5c283
Revises: daa1f747d3e3
Create Date: 2024-01-16 18:10:05.057075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe364ec5c283'
down_revision = 'daa1f747d3e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verificador_testes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('numero', sa.String(length=64), nullable=False),
    sa.Column('entrada', sa.String(length=250000), nullable=False),
    sa.Column('veredito', sa.Enum('OK', 'WA', 'PE', 'CA', name='vereditoverificadortesteenum'), nullable=False),
    sa.Column('verificador_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['verificador_id'], ['verificadores.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('verificador_id')
    )
    op.create_index(op.f('ix_verificador_testes_id'), 'verificador_testes', ['id'], unique=False)
    op.add_column('validador_testes', sa.Column('numero', sa.String(length=64), nullable=False))
    op.drop_column('validador_testes', 'codigo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('validador_testes', sa.Column('codigo', sa.VARCHAR(length=64), nullable=False))
    op.drop_column('validador_testes', 'numero')
    op.drop_index(op.f('ix_verificador_testes_id'), table_name='verificador_testes')
    op.drop_table('verificador_testes')
    # ### end Alembic commands ###