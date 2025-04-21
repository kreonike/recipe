"""Добавление user.patronomic

Revision ID: dd29c85f63be
Revises: 67d9989a3443
Create Date: 2025-04-18 09:30:33.678558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd29c85f63be'
down_revision: Union[str, None] = '67d9989a3443'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('patronomic', sa.String(length=50), nullable=True))



def downgrade() -> None:
    op.drop_column('users', 'patronomic')

