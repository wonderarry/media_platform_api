"""add post table

Revision ID: d5307e227008
Revises: 67e81edf63c3
Create Date: 2022-08-07 02:50:44.832118

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null, text
from sqlalchemy.types import TIMESTAMP
# revision identifiers, used by Alembic.
revision = 'd5307e227008'
down_revision = '67e81edf63c3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('betterposts',
    sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
    sa.Column('title', sa.String, nullable = False),
    sa.Column('content', sa.String, nullable = False),
    sa.Column('published', sa.Boolean, server_default = 'TRUE'),
    sa.Column('created_at', TIMESTAMP(timezone=True), server_default = text('now()'), nullable = False),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('betterusers.id', ondelete='CASCADE'), nullable = False),
    )



def downgrade() -> None:
    op.drop_table('betterposts')
