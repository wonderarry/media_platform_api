"""adding in other user columns

Revision ID: 67e81edf63c3
Revises: cfa2fa5970e1
Create Date: 2022-08-07 02:22:14.526251

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql.expression import null, text
# revision identifiers, used by Alembic.
revision = '67e81edf63c3'
down_revision = 'cfa2fa5970e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint('uq_betterusers_email', 'betterusers', ['email'], schema='public')
    op.add_column('betterusers', sa.Column('password', sa.String(), nullable = False))
    op.add_column('betterusers', sa.Column('created_at', TIMESTAMP(timezone=True), server_default = text('now()'), nullable = False))
    


def downgrade() -> None:
    #op.drop_constraint('uq_betterusers_email', 'betterusers')
    #op.drop_column('betterusers', 'password')
    #op.drop_column('betterusers', 'created_at')
    pass
