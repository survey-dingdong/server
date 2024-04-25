"""change order to order_no

Revision ID: 5ca10b8a1ad4
Revises: 04785df6dd6b
Create Date: 2024-04-26 00:27:22.581388

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "5ca10b8a1ad4"
down_revision = "04785df6dd6b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("workspace", sa.Column("order_no", sa.Integer(), nullable=False))
    op.drop_column("workspace", "order")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "workspace",
        sa.Column("order", mysql.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_column("workspace", "order_no")
    # ### end Alembic commands ###
