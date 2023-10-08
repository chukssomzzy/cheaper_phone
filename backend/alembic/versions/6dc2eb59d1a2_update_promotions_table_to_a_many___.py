"""update promotions table to a many _ many, add and removed some columns

Revision ID: 6dc2eb59d1a2
Revises: 20a2480da277
Create Date: 2023-10-08 20:31:16.681123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dc2eb59d1a2'
down_revision: Union[str, None] = '20a2480da277'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("promotions_ibfk_1", "promotions", type_="foreignkey")
    op.drop_column("promotions", "user_id")
    op.drop_column("promotions", "timestamp")
    op.drop_column("promotions", "action")

    op.create_table("product_promotions",
                    sa.Column("product_id", sa.String(60), primary_key=True),
                    sa.Column("promotion_id", sa.Integer, primary_key=True))
    with op.batch_alter_table("product_promotions") as batch_op:
        batch_op.create_foreign_key(
            "product_promotions_ibfk_1", "products",
            ["product_id"], ["id"])
        batch_op.create_foreign_key(
            "product_promotions_ibfk_2", "promotions", ["promotion_id"],
            ["id"])
    op.add_column("promotions", sa.Column(
        "name", sa.String(100), nullable=False))
    op.add_column("promotions", sa.Column(
        "start_date", sa.DateTime, nullable=False))
    op.add_column("promotions", sa.Column(
        "duration", sa.DateTime, nullable=False))
    op.add_column("promotions", sa.Column(
        "discount", sa.Integer, nullable=False))
    pass


def downgrade() -> None:
    op.add_column("promotions", sa.Column("user_id", sa.String(60)))
    op.create_foreign_key("promotions_ibfk_1", "promotions", "users", [
        "user_id"], ["id"])
    op.add_column("promotions", sa.Column(
        "timestamp", sa.DateTime, nullable=False))
    op.add_column("promotions", sa.Column(
        "action", sa.String(50), nullable=False))
    with op.batch_alter_table("product_promotions") as batch_op:
        batch_op.drop_constraint(
            "product_promotions_ibfk_1", type_="foreignkey")
        batch_op.drop_constraint(
            "product_promotions_ibfk_2", type_="foreignkey")
    op.drop_table("product_promotions")
    op.drop_column("promotions", "name")
    op.drop_column("promotions", "start_date")
    op.drop_column("promotions", "duration")
    op.drop_column("promotions", "discount")

    pass
