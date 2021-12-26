"""add api keys table

Revision ID: 1358959fd95c
Revises: c41493db69ab
Create Date: 2021-12-26 04:04:57.101231

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1358959fd95c'
down_revision = 'c41493db69ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api-keys',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_api-keys_id'), 'api-keys', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_api-keys_id'), table_name='api-keys')
    op.drop_table('api-keys')
    # ### end Alembic commands ###
