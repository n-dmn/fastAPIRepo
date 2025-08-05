"""initial tables"""

from alembic import op
import sqlalchemy as sa
import os


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

SCHEMA = os.getenv("DATABASE_SCHEMA", "app_schema")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(), nullable=False, unique=True),
        schema=SCHEMA,
    )
    op.create_table(
        "items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column(
            "owner_id",
            sa.Integer(),
            sa.ForeignKey(f"{SCHEMA}.users.id", name="fk_items_users_owner_id"),
            nullable=False,
        ),
        schema=SCHEMA,
    )


def downgrade() -> None:
    op.drop_table("items", schema=SCHEMA)
    op.drop_table("users", schema=SCHEMA)

