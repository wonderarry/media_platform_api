"""setting up vote table

Revision ID: 823cc3898f88
Revises: d5307e227008
Create Date: 2022-08-07 03:08:07.548726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '823cc3898f88'
down_revision = 'd5307e227008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('bettervotes',
    sa.Column('post_id', sa.Integer(), sa.ForeignKey('betterposts.id', ondelete='CASCADE'), primary_key = True, nullable = False),
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('betterusers.id', ondelete='CASCADE'), primary_key = True, nullable = False))
    


def downgrade() -> None:
    op.drop_table('bettervotes')
