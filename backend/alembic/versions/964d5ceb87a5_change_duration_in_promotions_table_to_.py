"""change duration in promotions table to string

Revision ID: 964d5ceb87a5
Revises: 1f04095c0f1a
Create Date: 2023-10-10 12:42:57.793922

"""
from datetime import timedelta
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '964d5ceb87a5'
down_revision: Union[str, None] = '1f04095c0f1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("promotions", "duration")
    op.add_column("promotions", sa.Column("duration", sa.String(
        50), nullable=False, default=str(timedelta(days=30))))
    pass


def downgrade() -> None:
    op.drop_column("promotions", "duration")
    op.add_column("promotions", sa.Column(
        "duration", sa.DateTime, nullable=False, default=timedelta(days=30)))
    pass
