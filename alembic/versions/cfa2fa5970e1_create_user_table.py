"""create user table

Revision ID: cfa2fa5970e1
Revises: 
Create Date: 2022-08-07 02:12:11.098965

"""

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'cfa2fa5970e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('betterposts', 
    sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
    sa.Column('email', sa.String(), nullable = False)
    )

def downgrade() -> None:
    op.drop_table('betterposts')
    pass
