"""Add a column

Revision ID: 2900d7c22ea2
Revises: 5901758228f0
Create Date: 2022-04-26 22:43:35.551838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2900d7c22ea2'
down_revision = '5901758228f0'
branch_labels = None
depends_on = None


from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')
