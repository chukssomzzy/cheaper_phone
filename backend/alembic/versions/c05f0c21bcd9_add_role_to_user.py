"""add role to user

Revision ID: c05f0c21bcd9
Revises: 955c51cfa13a
Create Date: 2023-09-10 14:06:07.471624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c05f0c21bcd9'
down_revision: Union[str, None] = '955c51cfa13a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """add column role to users table"""
    op.add_column("users", sa.Column("role", sa.Enum(
        "customer", "admin"), server_default="customer"))


def downgrade() -> None:
    """Drop column role from users table"""
    op.drop_column("users", "role")
