"""cria modelo de administrador

Revision ID: 38e402437b8f
Revises: 03d1ab6351f6
Create Date: 2024-02-06 00:57:09.327621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e402437b8f'
down_revision = '03d1ab6351f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('administradores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('administradores', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_administradores_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_administradores_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_administradores_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('administradores', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_administradores_username'))
        batch_op.drop_index(batch_op.f('ix_administradores_id'))
        batch_op.drop_index(batch_op.f('ix_administradores_email'))

    op.drop_table('administradores')
    # ### end Alembic commands ###
