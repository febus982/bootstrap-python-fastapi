"""Initialize fixture tables

Revision ID: 52b1246eda46
Revises:
Create Date: 2025-01-26 21:23:26.321986

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "52b1246eda46"
down_revision = None
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()[f"upgrade_{engine_name}"]()


def downgrade(engine_name: str) -> None:
    globals()[f"downgrade_{engine_name}"]()


def upgrade_default() -> None:
    op.create_table(
        "alembic_fixtures",
        sa.Column("bind", sa.String(length=255), nullable=False),
        sa.Column("module_name", sa.String(length=255), nullable=False),
        sa.Column("signature", sa.String(length=255), nullable=False),
        sa.Column("alembic_head_revisions", sa.String(length=255), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("bind", "module_name"),
    )


def downgrade_default() -> None:
    op.drop_table("alembic_fixtures")
