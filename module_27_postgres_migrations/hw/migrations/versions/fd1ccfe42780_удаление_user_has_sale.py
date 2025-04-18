"""Удаление user.has_sale

Revision ID: fd1ccfe42780
Revises: 321bdabf28bc
Create Date: 2025-04-18 09:25:07.056591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd1ccfe42780'
down_revision: Union[str, None] = '321bdabf28bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'has_sale')



def downgrade() -> None:
    op.add_column('users', sa.Column('has_sale', sa.Boolean(), nullable=True))

