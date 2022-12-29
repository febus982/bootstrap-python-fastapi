"""create books table

Revision ID: 52b1246eda46
Revises: 
Create Date: 2022-11-09 20:33:13.035514

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "52b1246eda46"
down_revision = None
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()


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
