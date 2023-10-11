"""add column stripe_customer_id to customer

Revision ID: 6456320a9b3e
Revises: 72ab960efd6f
Create Date: 2023-10-11 15:35:05.201832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6456320a9b3e'
down_revision: Union[str, None] = '72ab960efd6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("stripe_customer_id", sa.String(
        50), nullable=False, server_default="null"))
    pass


def downgrade() -> None:
    op.drop_column("users", "stripe_customer_id")
    pass
