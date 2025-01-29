"""Create books table

Revision ID: bd73bd8a2ac4
Revises: 52b1246eda46
Create Date: 2025-01-26 21:28:26.321986

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "bd73bd8a2ac4"
down_revision = "52b1246eda46"
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name: str) -> None:
    globals()[f"downgrade_{engine_name}"]()


def upgrade_default() -> None:
    op.create_table(
        "books",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=True),
        sa.Column("author_name", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("book_id"),
    )


def downgrade_default() -> None:
    op.drop_table("books")
