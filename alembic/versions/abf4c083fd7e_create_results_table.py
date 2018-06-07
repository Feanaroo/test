"""create results table

Revision ID: abf4c083fd7e
Revises: 
Create Date: 2017-10-16 18:24:24.418308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abf4c083fd7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'results',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('number', sa.Integer, nullable=False),
        sa.Column('text', sa.String(512), nullable=False),
        sa.Column('ins_date', sa.DateTime, default=sa.func.current_timestamp()),
    )

def downgrade():
    op.drop_table('results')
