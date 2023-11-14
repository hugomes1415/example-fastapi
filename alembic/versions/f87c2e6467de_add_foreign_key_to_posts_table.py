"""add foreign-key to posts table

Revision ID: f87c2e6467de
Revises: 38830dce52ce
Create Date: 2023-11-14 10:30:14.243545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f87c2e6467de'
down_revision: Union[str, None] = '38830dce52ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", 
                          referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')

    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
