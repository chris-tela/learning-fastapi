"""add content to post table

Revision ID: e39f4f3cc81d
Revises: 01f73d32c98b
Create Date: 2024-05-30 15:50:20.365083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e39f4f3cc81d'
down_revision: Union[str, None] = '01f73d32c98b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
