"""change product and user_cart relationship to a many to many

Revision ID: d3f44d443f5f
Revises: 19cbe978750d
Create Date: 2023-09-12 05:53:25.769486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3f44d443f5f'
down_revision: Union[str, None] = '19cbe978750d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('user_cart_ibfk_2', 'user_cart', type_="foreignkey")
    op.drop_column('user_cart', 'product_id')
    op.drop_column('user_cart', 'quantity')
    op.create_table('user_cart_products',
                    sa.Column('user_cart_id', sa.String(60),
                              nullable=False, primary_key=True),
                    sa.Column('product_id', sa.String(60),
                              nullable=False, primary_key=True),
                    sa.Column('quantity', sa.Integer)
                    )
    op.create_foreign_key("fk_user_cart_product", "user_cart_products",
                          "user_cart", ["user_cart_id"], ["id"],
                          ondelete="CASCADE")
    op.create_foreign_key("product_cart_idfk_2", "user_cart_products",
                          "products", ["product_id"], ["id"],
                          onupdate="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("fk_user_cart_product",
                       "user_cart_products", type_="foreignkey")
    op.drop_constraint("product_cart_idfk_2",
                       "user_cart_products", type_="foreignkey")
    op.drop_table('user_cart_products')
    op.add_column('user_cart', sa.Column('product_id', sa.String(60)))
    op.create_foreign_key('user_cart_ibfk_2', 'user_cart',
                          'products', ['product_id'], ['id'])
    op.add_column('user_cart', sa.Column('quantity', sa.Integer))
    pass
