"""Добавление user.surname

Revision ID: 67d9989a3443
Revises: fd1ccfe42780
Create Date: 2025-04-18 09:27:26.648765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67d9989a3443'
down_revision: Union[str, None] = 'fd1ccfe42780'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('surname', sa.String(length=50), nullable=True))



def downgrade() -> None:
    op.drop_column('users', 'surname')

