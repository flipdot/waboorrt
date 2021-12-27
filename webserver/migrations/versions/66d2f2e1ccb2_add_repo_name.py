"""add repo name

Revision ID: 66d2f2e1ccb2
Revises: 1358959fd95c
Create Date: 2021-12-27 00:38:37.866745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66d2f2e1ccb2'
down_revision = '1358959fd95c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('repositories', sa.Column('name', sa.String(), nullable=True))
    op.create_index(op.f('ix_repositories_name'), 'repositories', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_repositories_name'), table_name='repositories')
    op.drop_column('repositories', 'name')
    # ### end Alembic commands ###