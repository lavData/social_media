"""create account table

Revision ID: 5901758228f0
Revises: 
Create Date: 2022-04-26 22:38:29.134441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5901758228f0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
