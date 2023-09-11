"""remove column product_id from cart and add culumn cart_id to product

Revision ID: d74383e21f0f
Revises: 19cbe978750d
Create Date: 2023-09-11 07:15:08.667482

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd74383e21f0f'
down_revision: Union[str, None] = '19cbe978750d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key("fk_cart_product", "products",
                          "cart", ["cart_id"], ["id"])
    pass


def downgrade() -> None:
    pass
