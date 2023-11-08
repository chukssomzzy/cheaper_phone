"""add stripe id to table orders and product

Revision ID: 104736a992ec
Revises: 26bd6c0722b5
Create Date: 2023-11-07 20:34:47.658742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '104736a992ec'
down_revision: Union[str, None] = '26bd6c0722b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("orders", sa.Column(
        "stripe_orders_id", sa.String(100), unique=True))
    op.add_column("products", sa.Column(
        "stripe_products_id", sa.String(100), unique=True))


def downgrade() -> None:
    op.drop_column("orders", "stripe_orders_id")
    op.drop_column("products", "stripe_products_id")
