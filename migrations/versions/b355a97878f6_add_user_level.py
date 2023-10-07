"""Add user level

Revision ID: b355a97878f6
Revises: c0baaeee31f8
Create Date: 2023-10-06 20:30:58.206728

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b355a97878f6'
down_revision = 'c0baaeee31f8'
branch_labels = None
depends_on = None


def upgrade():
    user_level = postgresql.ENUM('bronze', 'silver', 'gold', name='user_level')
    user_level.create(op.get_bind())

    op.add_column('users', sa.Column('level', sa.Enum('bronze', 'silver', 'gold', name='user_level'), nullable=True))

def downgrade():
    op.drop_column('users', 'level')

    user_level = postgresql.ENUM('bronze', 'silver', 'gold', name='user_level')
    user_level.drop(op.get_bind())