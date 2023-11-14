"""add content column

Revision ID: 163930847d30
Revises: 0b34543c02bd
Create Date: 2023-11-14 09:46:28.513435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '163930847d30'
down_revision: Union[str, None] = '0b34543c02bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
