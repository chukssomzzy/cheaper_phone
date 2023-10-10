"""add column isexpired to promotions table

Revision ID: 72ab960efd6f
Revises: 964d5ceb87a5
Create Date: 2023-10-10 15:46:54.948683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72ab960efd6f'
down_revision: Union[str, None] = '964d5ceb87a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("promotions", sa.Column("isexpired",
                                          sa.Boolean, nullable=False,
                                          default=False))


def downgrade() -> None:
    op.drop_column("promotion", "isexpired")
