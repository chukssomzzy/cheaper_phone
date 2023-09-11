"""add _pwd_hash and _salt to users table

Revision ID: 955c51cfa13a
Revises:
Create Date: 2023-09-10 10:56:16.367161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '955c51cfa13a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """adds _pwd_hash column to users table"""
    op.add_column("users", sa.Column("_pwd_hash", sa.String(
        128), nullable=False, server_default=""))
    op.add_column("users", sa.Column("_salt", sa.String(32),
                  nullable=False, server_default=""))


def downgrade() -> None:
    """Drops _pwd_hash and _salt column from users table"""
    op.drop_column('users', '_pwd_hash')
    op.drop_column('users', '_salt')
    pass
