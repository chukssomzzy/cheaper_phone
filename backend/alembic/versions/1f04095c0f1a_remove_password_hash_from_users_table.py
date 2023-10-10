"""remove password_hash from users table

Revision ID: 1f04095c0f1a
Revises: 6dc2eb59d1a2
Create Date: 2023-10-09 21:07:42.479203

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f04095c0f1a'
down_revision: Union[str, None] = '6dc2eb59d1a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "password_hash")
    pass


def downgrade() -> None:
    op.add_column("users", sa.Column("password_hash",
                  sa.String(50)))
    pass
