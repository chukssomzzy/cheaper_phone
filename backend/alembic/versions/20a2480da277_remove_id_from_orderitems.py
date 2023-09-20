"""remove id from orderitems

Revision ID: 20a2480da277
Revises: 08e64de8550f
Create Date: 2023-09-20 16:05:35.611851

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20a2480da277'
down_revision: Union[str, None] = '08e64de8550f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("order_items", "id")
    pass


def downgrade() -> None:
    op.add_column("order_items", sa.Column(
        "id", sa.String(60), default=uuid4(), primary_key=True))
    pass
