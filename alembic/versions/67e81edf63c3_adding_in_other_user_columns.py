"""adding in other user columns

Revision ID: 67e81edf63c3
Revises: cfa2fa5970e1
Create Date: 2022-08-07 02:22:14.526251

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.types import TIMESTAMP

# revision identifiers, used by Alembic.
revision = '67e81edf63c3'
down_revision = 'cfa2fa5970e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint('uq_betterposts_email', 'betterposts', ['email'], schema='public')
    op.add_column('betterposts', sa.Column('password', sa.String(), nullable = False))
    op.add_column('betterposts', sa.Column('created_at', TIMESTAMP(timezone=True), server_default = sa.text('now()'), nullable = False))
    


def downgrade() -> None:
    op.drop_constraint('uq_betterposts_email')
    op.drop_column('betterposts', 'password')
    op.drop_column('betterposts', 'created_at')
