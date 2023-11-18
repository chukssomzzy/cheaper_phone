"""make phone_number column in shipping_address table nullable

Revision ID: 95fa3dd186db
Revises: 104736a992ec
Create Date: 2023-11-18 16:16:54.567312

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95fa3dd186db'
down_revision: Union[str, None] = '104736a992ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("shipping_address", "phone_number",
                    nullable=True, existing_type=sa.String(20))


def downgrade() -> None:
    op.alter_column("shipping_address", "phone_number",
                    nullable=False, existing_type=sa.String(20))
