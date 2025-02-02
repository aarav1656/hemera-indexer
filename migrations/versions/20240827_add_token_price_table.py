"""add token price table

Revision ID: 2359a28d63cb
Revises: bf51d23c852f
Create Date: 2024-08-27 17:58:50.838313

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2359a28d63cb"
down_revision: Union[str, None] = "bf51d23c852f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "token_hourly_prices",
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=True),
        sa.PrimaryKeyConstraint("symbol", "timestamp"),
        if_not_exists=True,
    )

    op.create_table(
        "token_prices",
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=True),
        sa.PrimaryKeyConstraint("symbol", "timestamp"),
        if_not_exists=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
