"""add last few columns to possts table

Revision ID: d23fbbb9646f
Revises: f87c2e6467de
Create Date: 2023-11-14 11:28:02.028261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd23fbbb9646f'
down_revision: Union[str, None] = 'f87c2e6467de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('pub', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts',
                  sa.Column('creat', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'pub')
    op.drop_column('posts', 'creat')
    pass
