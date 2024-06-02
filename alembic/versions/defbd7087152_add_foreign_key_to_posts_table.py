"""add foreign-key to posts table

Revision ID: defbd7087152
Revises: 1584ee19ca67
Create Date: 2024-06-01 17:32:26.297839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'defbd7087152'
down_revision: Union[str, None] = '1584ee19ca67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('owner_id', sa.Integer, nullable=False))
    # name of foreign key, source table of foreign key, reference the remote table
    op.create_foreign_key('post_users_fk', source_table = "posts", referent_table="users", local_cols=['owner_id'], remote_cols=["id"], ondelete="CASCADE" )
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
