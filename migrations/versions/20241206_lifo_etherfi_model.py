"""lido_share_balance_d,lido_position_values_d,lido_share_balance_current_d,ether_fi_share_balance_d,ether_fi_share_balance_current_d,ether_fi_position_values_d,ether_fi_lrt_exchange_rate_d

Revision ID: 25a7152fdde4
Revises: 3bd2e3099bae
Create Date: 2024-12-06 16:11:44.574524

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "25a7152fdde4"
down_revision: Union[str, None] = "3bd2e3099bae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "af_eigen_layer_address_current",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("strategy", postgresql.BYTEA(), nullable=False),
        sa.Column("token", postgresql.BYTEA(), nullable=True),
        sa.Column("deposit_amount", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("start_withdraw_amount", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("finish_withdraw_amount", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("address", "strategy"),
        if_not_exists=True,
    )
    op.create_table(
        "af_eigen_layer_records",
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=False),
        sa.Column("log_index", sa.INTEGER(), nullable=False),
        sa.Column("internal_idx", sa.INTEGER(), nullable=False),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("method", sa.VARCHAR(), nullable=True),
        sa.Column("event_name", sa.VARCHAR(), nullable=True),
        sa.Column("strategy", postgresql.BYTEA(), nullable=True),
        sa.Column("token", postgresql.BYTEA(), nullable=True),
        sa.Column("staker", postgresql.BYTEA(), nullable=True),
        sa.Column("shares", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("withdrawer", postgresql.BYTEA(), nullable=True),
        sa.Column("withdrawroot", postgresql.BYTEA(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("transaction_hash", "log_index", "internal_idx"),
        if_not_exists=True,
    )
    op.create_table(
        "af_ether_fi_lrt_exchange_rate",
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("exchange_rate", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=False),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("token_address", "block_number"),
        if_not_exists=True,
    )
    op.create_table(
        "af_ether_fi_position_values",
        sa.Column("block_number", sa.BIGINT(), nullable=False),
        sa.Column("total_share", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("total_value_out_lp", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("total_value_in_lp", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("block_number"),
        if_not_exists=True,
    )
    op.create_table(
        "af_ether_fi_share_balances",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("shares", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=False),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("address", "token_address", "block_number"),
        if_not_exists=True,
    )
    op.create_table(
        "af_ether_fi_share_balances_current",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("shares", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("address", "token_address"),
        if_not_exists=True,
    )
    op.create_table(
        "af_karak_address_current",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("vault", postgresql.BYTEA(), nullable=False),
        sa.Column("deposit_amount", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("start_withdraw_amount", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("finish_withdraw_amount", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("d_s", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("d_f", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("s_f", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("address", "vault"),
        if_not_exists=True,
    )
    op.create_table(
        "af_karak_records",
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=False),
        sa.Column("log_index", sa.INTEGER(), nullable=False),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("method", sa.VARCHAR(), nullable=True),
        sa.Column("event_name", sa.VARCHAR(), nullable=True),
        sa.Column("topic0", sa.VARCHAR(), nullable=True),
        sa.Column("from_address", postgresql.BYTEA(), nullable=True),
        sa.Column("to_address", postgresql.BYTEA(), nullable=True),
        sa.Column("token", sa.VARCHAR(), nullable=True),
        sa.Column("vault", postgresql.BYTEA(), nullable=True),
        sa.Column("amount", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("balance", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("staker", sa.VARCHAR(), nullable=True),
        sa.Column("operator", sa.VARCHAR(), nullable=True),
        sa.Column("withdrawer", sa.VARCHAR(), nullable=True),
        sa.Column("shares", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("withdrawroot", sa.VARCHAR(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("transaction_hash", "log_index"),
        if_not_exists=True,
    )
    op.create_table(
        "af_karak_vault_token",
        sa.Column("vault", postgresql.BYTEA(), nullable=False),
        sa.Column("token", postgresql.BYTEA(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.Column("symbol", sa.VARCHAR(), nullable=True),
        sa.Column("asset_type", sa.INTEGER(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("vault", "token"),
        if_not_exists=True,
    )
    op.create_table(
        "af_lido_position_values",
        sa.Column("block_number", sa.BIGINT(), nullable=False),
        sa.Column("total_share", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("buffered_eth", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("consensus_layer", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("deposited_validators", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("cl_validators", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("block_number"),
        if_not_exists=True,
    )
    op.create_table(
        "af_lido_seth_share_balances",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("shares", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=False),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("address", "token_address", "block_number"),
        if_not_exists=True,
    )
    op.create_table(
        "af_lido_seth_share_balances_current",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("shares", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("address", "token_address"),
        if_not_exists=True,
    )
    op.create_table(
        "af_project_contracts",
        sa.Column("project_id", sa.VARCHAR(), nullable=True),
        sa.Column("chain_id", sa.INTEGER(), nullable=True),
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("deployer", postgresql.BYTEA(), nullable=True),
        sa.Column("transaction_from_address", postgresql.BYTEA(), nullable=True),
        sa.Column("trace_creator", postgresql.BYTEA(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), nullable=True),
        sa.PrimaryKeyConstraint("address"),
        if_not_exists=True,
    )
    op.create_table(
        "af_projects",
        sa.Column("project_id", sa.VARCHAR(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.Column("deployer", postgresql.BYTEA(), nullable=False),
        sa.Column("address_type", sa.INTEGER(), nullable=True, comment="0是作为deploy地址不参与统计；1参与统计"),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("project_id", "deployer"),
        if_not_exists=True,
    )
    op.create_table(
        "cyber_address",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.Column("reverse_node", postgresql.BYTEA(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("address"),
        if_not_exists=True,
    )
    op.create_table(
        "cyber_id_record",
        sa.Column("node", postgresql.BYTEA(), nullable=False),
        sa.Column("token_id", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("label", sa.VARCHAR(), nullable=True),
        sa.Column("registration", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("address", postgresql.BYTEA(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("cost", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("node"),
        if_not_exists=True,
    )
    op.drop_table("erc721_token_mint", if_exists=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "erc721_token_mint",
        sa.Column("token_address", postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column("token_id", sa.NUMERIC(), autoincrement=False, nullable=False),
        sa.Column("block_number", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column("transaction_hash", postgresql.BYTEA(), autoincrement=False, nullable=False),
        sa.Column(
            "create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), autoincrement=False, nullable=True
        ),
        sa.Column(
            "update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), autoincrement=False, nullable=True
        ),
        sa.Column("reorg", sa.BOOLEAN(), server_default=sa.text("false"), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("token_address", "token_id", name="erc721_token_mint_pkey"),
        if_not_exists=True,
    )
    op.drop_table("cyber_id_record", if_exists=True)
    op.drop_table("cyber_address", if_exists=True)
    op.drop_table("af_projects", if_exists=True)
    op.drop_table("af_project_contracts", if_exists=True)
    op.drop_table("af_lido_seth_share_balances_current", if_exists=True)
    op.drop_table("af_lido_seth_share_balances", if_exists=True)
    op.drop_table("af_lido_position_values", if_exists=True)
    op.drop_table("af_karak_vault_token", if_exists=True)
    op.drop_table("af_karak_records", if_exists=True)
    op.drop_table("af_karak_address_current", if_exists=True)
    op.drop_table("af_ether_fi_share_balances_current", if_exists=True)
    op.drop_table("af_ether_fi_share_balances", if_exists=True)
    op.drop_table("af_ether_fi_position_values", if_exists=True)
    op.drop_table("af_ether_fi_lrt_exchange_rate", if_exists=True)
    op.drop_table("af_eigen_layer_records", if_exists=True)
    op.drop_table("af_eigen_layer_address_current", if_exists=True)
    # ### end Alembic commands ###
