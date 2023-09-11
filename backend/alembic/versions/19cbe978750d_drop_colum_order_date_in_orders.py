"""drop colum order_date in orders

Revision ID: 19cbe978750d
Revises: c05f0c21bcd9
Create Date: 2023-09-11 05:55:57.367291

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19cbe978750d'
down_revision: Union[str, None] = 'c05f0c21bcd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('orders', 'order_date')
    pass


def downgrade() -> None:
    op.add_column('orders', sa.Column(sa.DATETIME, default=datetime.utcnow))
    pass
