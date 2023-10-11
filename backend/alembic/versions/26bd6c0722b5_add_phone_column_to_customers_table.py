"""add phone column to customers table

Revision ID: 26bd6c0722b5
Revises: 6456320a9b3e
Create Date: 2023-10-11 16:02:46.189003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26bd6c0722b5'
down_revision: Union[str, None] = '6456320a9b3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column(
        "phone", sa.String(20), server_default="null"))
    pass


def downgrade() -> None:
    op.drop_column("users", "phone")
    pass
