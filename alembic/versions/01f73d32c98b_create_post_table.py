"""create post table

Revision ID: 01f73d32c98b
Revises: 21725a852214
Create Date: 2024-05-30 15:30:52.188541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01f73d32c98b'
down_revision: Union[str, None] = '21725a852214'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#post table
def upgrade() -> None:
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable =False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
