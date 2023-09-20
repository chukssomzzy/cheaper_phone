"""add defualt column to shipping address

Revision ID: 08e64de8550f
Revises: 63a813062385
Create Date: 2023-09-17 19:40:39.537321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08e64de8550f'
down_revision: Union[str, None] = '63a813062385'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("shipping_address", sa.Column(
        "default", sa.Boolean, nullable=False, default=False))
    pass


def downgrade() -> None:
    op.drop_column("shipping_address", "default")
    pass
