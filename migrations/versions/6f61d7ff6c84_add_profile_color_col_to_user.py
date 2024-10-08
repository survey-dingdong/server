"""add profile color col to user

Revision ID: 6f61d7ff6c84
Revises: 017396941c7b
Create Date: 2024-07-15 01:04:26.565774

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "6f61d7ff6c84"
down_revision = "017396941c7b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column("user", "profile_color")
    op.add_column(
        "user", sa.Column("profile_color", sa.String(length=7), nullable=True)
    )
    op.execute(
        """
        UPDATE user
        SET profile_color =
            CASE FLOOR(1 + RAND() * 6)
                WHEN 1 THEN '#3F57FD'
                WHEN 2 THEN '#DB5654'
                WHEN 3 THEN '#613EE2'
                WHEN 4 THEN '#FD3F78'
                WHEN 5 THEN '#F08F1D'
                WHEN 6 THEN '#24A29A'
            END;
        """
    )
    op.alter_column(
        "user",
        "profile_color",
        existing_type=mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=7),
        type_=sa.String(length=7),
        existing_nullable=True,
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "profile_color")
    # ### end Alembic commands ###
