"""add column created and updated_at in user_cart_product

Revision ID: 63a813062385
Revises: d3f44d443f5f
Create Date: 2023-09-17 10:08:48.962084

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63a813062385'
down_revision: Union[str, None] = 'd3f44d443f5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("user_cart_products", sa.Column(
        "created_at", sa.DateTime, default=datetime.utcnow))
    op.add_column("user_cart_products", sa.Column(
        "updated_at", sa.DateTime, default=datetime.utcnow))
    pass


def downgrade() -> None:
    op.drop_column("user_cart_products", "created_at")
    op.drop_column("user_cart_products", "updated_at")
    pass
