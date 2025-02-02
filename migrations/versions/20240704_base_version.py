"""base version

Revision ID: 5e4608933f64
Revises:
Create Date: 2024-07-04 19:05:00.122248

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "5e4608933f64"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "address_coin_balances",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("balance", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=False),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("address", "block_number"),
    )
    op.create_table(
        "address_token_balances",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_id", sa.NUMERIC(precision=78), nullable=True),
        sa.Column("token_type", sa.VARCHAR(), nullable=True),
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("balance", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=False),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("address", "token_address", "token_id", "block_number"),
    )
    op.create_table(
        "block_ts_mapper",
        sa.Column("ts", sa.BIGINT(), nullable=False),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("ts"),
    )
    op.create_index(
        "block_ts_mapper_idx",
        "block_ts_mapper",
        [sa.text("block_number DESC")],
        unique=False,
    )
    op.create_table(
        "blocks",
        sa.Column("hash", postgresql.BYTEA(), nullable=False),
        sa.Column("number", sa.BIGINT(), nullable=True),
        sa.Column("timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("parent_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("nonce", postgresql.BYTEA(), nullable=True),
        sa.Column("gas_limit", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("gas_used", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("base_fee_per_gas", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("difficulty", sa.NUMERIC(precision=38), nullable=True),
        sa.Column("total_difficulty", sa.NUMERIC(precision=38), nullable=True),
        sa.Column("size", sa.BIGINT(), nullable=True),
        sa.Column("miner", postgresql.BYTEA(), nullable=True),
        sa.Column("sha3_uncles", postgresql.BYTEA(), nullable=True),
        sa.Column("transactions_root", postgresql.BYTEA(), nullable=True),
        sa.Column("transactions_count", sa.BIGINT(), nullable=True),
        sa.Column("state_root", postgresql.BYTEA(), nullable=True),
        sa.Column("receipts_root", postgresql.BYTEA(), nullable=True),
        sa.Column("extra_data", postgresql.BYTEA(), nullable=True),
        sa.Column("withdrawals_root", postgresql.BYTEA(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("hash"),
    )
    op.create_index("blocks_number_index", "blocks", [sa.text("number DESC")], unique=False)
    op.create_index("blocks_timestamp_index", "blocks", [sa.text("timestamp DESC")], unique=False)
    op.create_table(
        "contract_internal_transactions",
        sa.Column("trace_id", sa.VARCHAR(), nullable=False),
        sa.Column("from_address", postgresql.BYTEA(), nullable=True),
        sa.Column("to_address", postgresql.BYTEA(), nullable=True),
        sa.Column("value", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("trace_type", sa.VARCHAR(), nullable=True),
        sa.Column("call_type", sa.VARCHAR(), nullable=True),
        sa.Column("gas", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("gas_used", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("trace_address", postgresql.ARRAY(sa.INTEGER()), nullable=True),
        sa.Column("error", sa.TEXT(), nullable=True),
        sa.Column("status", sa.INTEGER(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("transaction_index", sa.INTEGER(), nullable=True),
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("trace_id"),
    )
    op.create_index(
        "contract_internal_transactions_transaction_hash_idx",
        "contract_internal_transactions",
        ["transaction_hash"],
        unique=False,
    )
    op.create_index(
        "internal_transactions_address_number_transaction_index",
        "contract_internal_transactions",
        [
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("transaction_index DESC"),
        ],
        unique=False,
    )
    op.create_index(
        "internal_transactions_block_timestamp_index",
        "contract_internal_transactions",
        [sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.create_table(
        "contracts",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.Column("contract_creator", postgresql.BYTEA(), nullable=True),
        sa.Column("creation_code", postgresql.BYTEA(), nullable=True),
        sa.Column("deployed_code", postgresql.BYTEA(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("transaction_index", sa.INTEGER(), nullable=True),
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("official_website", sa.VARCHAR(), nullable=True),
        sa.Column("description", sa.VARCHAR(), nullable=True),
        sa.Column("email", sa.VARCHAR(), nullable=True),
        sa.Column("social_list", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("is_verified", sa.BOOLEAN(), nullable=True),
        sa.Column("is_proxy", sa.BOOLEAN(), nullable=True),
        sa.Column("implementation_contract", postgresql.BYTEA(), nullable=True),
        sa.Column("verified_implementation_contract", postgresql.BYTEA(), nullable=True),
        sa.Column("proxy_standard", sa.VARCHAR(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("address"),
    )
    op.create_table(
        "erc1155_token_holders",
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("wallet_address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_id", sa.NUMERIC(precision=78), nullable=False),
        sa.Column("balance_of", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("latest_call_contract_time", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("token_address", "wallet_address", "token_id"),
    )
    op.create_index(
        "erc1155_token_holders_token_address_balance_of_index",
        "erc1155_token_holders",
        ["token_address", sa.text("balance_of DESC")],
        unique=False,
    )
    op.create_table(
        "erc1155_token_id_details",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_id", sa.NUMERIC(precision=78), nullable=False),
        sa.Column("token_supply", sa.NUMERIC(precision=78), nullable=True),
        sa.Column("token_uri", sa.VARCHAR(), nullable=True),
        sa.Column("token_uri_info", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("address", "token_id"),
    )
    op.create_index(
        "erc1155_detail_desc_address_id_index",
        "erc1155_token_id_details",
        [sa.text("address DESC"), "token_id"],
        unique=False,
    )
    op.create_table(
        "erc1155_token_transfers",
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=False),
        sa.Column("log_index", sa.INTEGER(), nullable=False),
        sa.Column("from_address", postgresql.BYTEA(), nullable=True),
        sa.Column("to_address", postgresql.BYTEA(), nullable=True),
        sa.Column("token_address", postgresql.BYTEA(), nullable=True),
        sa.Column("token_id", sa.NUMERIC(precision=78), nullable=True),
        sa.Column("value", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("transaction_hash", "log_index"),
    )
    op.create_index(
        "erc1155_token_transfers_address_block_number_log_index_index",
        "erc1155_token_transfers",
        [
            "token_address",
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("log_index DESC"),
        ],
        unique=False,
    )
    op.create_index(
        "erc1155_token_transfers_block_timestamp_index",
        "erc1155_token_transfers",
        [sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.create_table(
        "erc20_token_holders",
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("wallet_address", postgresql.BYTEA(), nullable=False),
        sa.Column("balance_of", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("token_address", "wallet_address"),
    )
    op.create_index(
        "erc20_token_holders_token_address_balance_of_index",
        "erc20_token_holders",
        ["token_address", sa.text("balance_of DESC")],
        unique=False,
    )
    op.create_table(
        "erc20_token_transfers",
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=False),
        sa.Column("log_index", sa.INTEGER(), nullable=False),
        sa.Column("from_address", postgresql.BYTEA(), nullable=True),
        sa.Column("to_address", postgresql.BYTEA(), nullable=True),
        sa.Column("token_address", postgresql.BYTEA(), nullable=True),
        sa.Column("value", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("transaction_hash", "log_index"),
    )
    op.create_index(
        "erc20_token_transfers_address_block_number_log_index_index",
        "erc20_token_transfers",
        [
            "token_address",
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("log_index DESC"),
        ],
        unique=False,
    )
    op.create_index(
        "erc20_token_transfers_block_timestamp_index",
        "erc20_token_transfers",
        [sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.create_table(
        "erc721_token_holders",
        sa.Column("token_address", postgresql.BYTEA(), nullable=False),
        sa.Column("wallet_address", postgresql.BYTEA(), nullable=False),
        sa.Column("balance_of", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("token_address", "wallet_address"),
    )
    op.create_index(
        "erc721_token_holders_token_address_balance_of_index",
        "erc721_token_holders",
        ["token_address", sa.text("balance_of DESC")],
        unique=False,
    )
    op.create_table(
        "erc721_token_id_changes",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_id", sa.NUMERIC(precision=78), nullable=False),
        sa.Column("token_owner", postgresql.BYTEA(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=False),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("address", "token_id", "block_number"),
    )
    op.create_index(
        "erc721_change_address_id_number_desc_index",
        "erc721_token_id_changes",
        ["address", "token_id", sa.text("block_number DESC")],
        unique=False,
    )
    op.create_table(
        "erc721_token_id_details",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("token_id", sa.NUMERIC(precision=78), nullable=False),
        sa.Column("token_owner", postgresql.BYTEA(), nullable=True),
        sa.Column("token_uri", sa.VARCHAR(), nullable=True),
        sa.Column("token_uri_info", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("address", "token_id"),
    )
    op.create_index(
        "erc721_detail_owner_address_id_index",
        "erc721_token_id_details",
        [sa.text("token_owner DESC"), "address", "token_id"],
        unique=False,
    )
    op.create_table(
        "erc721_token_transfers",
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=False),
        sa.Column("log_index", sa.INTEGER(), nullable=False),
        sa.Column("from_address", postgresql.BYTEA(), nullable=True),
        sa.Column("to_address", postgresql.BYTEA(), nullable=True),
        sa.Column("token_address", postgresql.BYTEA(), nullable=True),
        sa.Column("token_id", sa.NUMERIC(precision=78), nullable=True),
        sa.Column("token_uri", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("transaction_hash", "log_index"),
    )
    op.create_index(
        "erc721_token_transfers_address_block_number_log_index_index",
        "erc721_token_transfers",
        [
            "token_address",
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("log_index DESC"),
        ],
        unique=False,
    )
    op.create_index(
        "erc721_token_transfers_block_timestamp_index",
        "erc721_token_transfers",
        [sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.create_table(
        "fix_record",
        sa.Column("job_id", sa.INTEGER(), nullable=False),
        sa.Column("start_block_number", sa.BIGINT(), nullable=True),
        sa.Column("last_fixed_block_number", sa.BIGINT(), nullable=True),
        sa.Column("remain_process", sa.INTEGER(), nullable=True),
        sa.Column("job_status", sa.VARCHAR(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("job_id"),
    )
    op.create_table(
        "logs",
        sa.Column("log_index", sa.INTEGER(), nullable=False),
        sa.Column("address", postgresql.BYTEA(), nullable=True),
        sa.Column("data", postgresql.BYTEA(), nullable=True),
        sa.Column("topic0", postgresql.BYTEA(), nullable=True),
        sa.Column("topic1", postgresql.BYTEA(), nullable=True),
        sa.Column("topic2", postgresql.BYTEA(), nullable=True),
        sa.Column("topic3", postgresql.BYTEA(), nullable=True),
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=False),
        sa.Column("transaction_index", sa.INTEGER(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("log_index", "transaction_hash"),
    )
    op.create_index(
        "logs_address_block_number_log_index_index",
        "logs",
        ["address", sa.text("block_number DESC"), sa.text("log_index DESC")],
        unique=False,
    )
    op.create_index(
        "logs_block_timestamp_index",
        "logs",
        [sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.create_table(
        "sync_record",
        sa.Column("mission_type", sa.VARCHAR(), nullable=False),
        sa.Column("entity_types", sa.INTEGER(), nullable=False),
        sa.Column("last_block_number", sa.BIGINT(), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("mission_type", "entity_types"),
    )
    op.create_table(
        "tokens",
        sa.Column("address", postgresql.BYTEA(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=True),
        sa.Column("symbol", sa.VARCHAR(), nullable=True),
        sa.Column("total_supply", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("decimals", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("token_type", sa.VARCHAR(), nullable=True),
        sa.Column("holder_count", sa.INTEGER(), nullable=True),
        sa.Column("transfer_count", sa.INTEGER(), nullable=True),
        sa.Column("icon_url", sa.VARCHAR(), nullable=True),
        sa.Column("urls", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("volume_24h", sa.NUMERIC(precision=38, scale=2), nullable=True),
        sa.Column("price", sa.NUMERIC(precision=38, scale=6), nullable=True),
        sa.Column("previous_price", sa.NUMERIC(precision=38, scale=6), nullable=True),
        sa.Column("market_cap", sa.NUMERIC(precision=38, scale=2), nullable=True),
        sa.Column("on_chain_market_cap", sa.NUMERIC(precision=38, scale=2), nullable=True),
        sa.Column("is_verified", sa.BOOLEAN(), nullable=True),
        sa.Column("cmc_id", sa.INTEGER(), nullable=True),
        sa.Column("cmc_slug", sa.VARCHAR(), nullable=True),
        sa.Column("gecko_id", sa.VARCHAR(), nullable=True),
        sa.Column("description", sa.VARCHAR(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("address"),
    )
    op.create_index("tokens_symbol_index", "tokens", ["symbol"], unique=False)
    op.create_index("tokens_type_index", "tokens", ["token_type"], unique=False)
    op.create_table(
        "traces",
        sa.Column("trace_id", sa.VARCHAR(), nullable=False),
        sa.Column("from_address", postgresql.BYTEA(), nullable=True),
        sa.Column("to_address", postgresql.BYTEA(), nullable=True),
        sa.Column("value", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("input", postgresql.BYTEA(), nullable=True),
        sa.Column("output", postgresql.BYTEA(), nullable=True),
        sa.Column("trace_type", sa.VARCHAR(), nullable=True),
        sa.Column("call_type", sa.VARCHAR(), nullable=True),
        sa.Column("gas", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("gas_used", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("subtraces", sa.INTEGER(), nullable=True),
        sa.Column("trace_address", postgresql.ARRAY(sa.INTEGER()), nullable=True),
        sa.Column("error", sa.TEXT(), nullable=True),
        sa.Column("status", sa.INTEGER(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("transaction_index", sa.INTEGER(), nullable=True),
        sa.Column("transaction_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("trace_id"),
    )
    op.create_index(
        "traces_address_block_timestamp_index",
        "traces",
        ["from_address", "to_address", sa.text("block_timestamp DESC")],
        unique=False,
    )
    op.create_index("traces_transaction_hash_index", "traces", ["transaction_hash"], unique=False)
    op.create_table(
        "transactions",
        sa.Column("hash", postgresql.BYTEA(), nullable=False),
        sa.Column("transaction_index", sa.INTEGER(), nullable=True),
        sa.Column("from_address", postgresql.BYTEA(), nullable=True),
        sa.Column("to_address", postgresql.BYTEA(), nullable=True),
        sa.Column("value", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("transaction_type", sa.INTEGER(), nullable=True),
        sa.Column("input", postgresql.BYTEA(), nullable=True),
        sa.Column("nonce", sa.INTEGER(), nullable=True),
        sa.Column("block_hash", postgresql.BYTEA(), nullable=True),
        sa.Column("block_number", sa.BIGINT(), nullable=True),
        sa.Column("block_timestamp", postgresql.TIMESTAMP(), nullable=True),
        sa.Column("gas", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("gas_price", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("max_fee_per_gas", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("max_priority_fee_per_gas", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("receipt_root", postgresql.BYTEA(), nullable=True),
        sa.Column("receipt_status", sa.INTEGER(), nullable=True),
        sa.Column("receipt_gas_used", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("receipt_cumulative_gas_used", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("receipt_effective_gas_price", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("receipt_l1_fee", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("receipt_l1_fee_scalar", sa.NUMERIC(precision=100, scale=18), nullable=True),
        sa.Column("receipt_l1_gas_used", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("receipt_l1_gas_price", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("receipt_blob_gas_used", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("receipt_blob_gas_price", sa.NUMERIC(precision=100), nullable=True),
        sa.Column("blob_versioned_hashes", postgresql.ARRAY(postgresql.BYTEA()), nullable=True),
        sa.Column("receipt_contract_address", postgresql.BYTEA(), nullable=True),
        sa.Column("exist_error", sa.BOOLEAN(), nullable=True),
        sa.Column("error", sa.TEXT(), nullable=True),
        sa.Column("revert_reason", sa.TEXT(), nullable=True),
        sa.Column("create_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("update_time", postgresql.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.Column("reorg", sa.BOOLEAN(), nullable=True, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("hash"),
    )
    op.create_index(
        "transactions_address_block_number_transaction_idx",
        "transactions",
        [
            "from_address",
            "to_address",
            sa.text("block_number DESC"),
            sa.text("transaction_index DESC"),
        ],
        unique=False,
    )
    op.create_index(
        "transactions_block_timestamp_block_number_index",
        "transactions",
        [sa.text("block_timestamp DESC"), sa.text("block_number DESC")],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("transactions_block_timestamp_block_number_index", table_name="transactions")
    op.drop_index("transactions_address_block_number_transaction_idx", table_name="transactions")
    op.drop_table("transactions")
    op.drop_index("traces_transaction_hash_index", table_name="traces")
    op.drop_index("traces_address_block_timestamp_index", table_name="traces")
    op.drop_table("traces")
    op.drop_index("tokens_type_index", table_name="tokens")
    op.drop_index("tokens_symbol_index", table_name="tokens")
    op.drop_table("tokens")
    op.drop_table("sync_record")
    op.drop_index("logs_block_timestamp_index", table_name="logs")
    op.drop_index("logs_address_block_number_log_index_index", table_name="logs")
    op.drop_table("logs")
    op.drop_table("fix_record")
    op.drop_index(
        "erc721_token_transfers_block_timestamp_index",
        table_name="erc721_token_transfers",
    )
    op.drop_index(
        "erc721_token_transfers_address_block_number_log_index_index",
        table_name="erc721_token_transfers",
    )
    op.drop_table("erc721_token_transfers")
    op.drop_index("erc721_detail_owner_address_id_index", table_name="erc721_token_id_details")
    op.drop_table("erc721_token_id_details")
    op.drop_index(
        "erc721_change_address_id_number_desc_index",
        table_name="erc721_token_id_changes",
    )
    op.drop_table("erc721_token_id_changes")
    op.drop_index(
        "erc721_token_holders_token_address_balance_of_index",
        table_name="erc721_token_holders",
    )
    op.drop_table("erc721_token_holders")
    op.drop_index(
        "erc20_token_transfers_block_timestamp_index",
        table_name="erc20_token_transfers",
    )
    op.drop_index(
        "erc20_token_transfers_address_block_number_log_index_index",
        table_name="erc20_token_transfers",
    )
    op.drop_table("erc20_token_transfers")
    op.drop_index(
        "erc20_token_holders_token_address_balance_of_index",
        table_name="erc20_token_holders",
    )
    op.drop_table("erc20_token_holders")
    op.drop_index(
        "erc1155_token_transfers_block_timestamp_index",
        table_name="erc1155_token_transfers",
    )
    op.drop_index(
        "erc1155_token_transfers_address_block_number_log_index_index",
        table_name="erc1155_token_transfers",
    )
    op.drop_table("erc1155_token_transfers")
    op.drop_index("erc1155_detail_desc_address_id_index", table_name="erc1155_token_id_details")
    op.drop_table("erc1155_token_id_details")
    op.drop_index(
        "erc1155_token_holders_token_address_balance_of_index",
        table_name="erc1155_token_holders",
    )
    op.drop_table("erc1155_token_holders")
    op.drop_table("contracts")
    op.drop_index(
        "internal_transactions_block_timestamp_index",
        table_name="contract_internal_transactions",
    )
    op.drop_index(
        "internal_transactions_address_number_transaction_index",
        table_name="contract_internal_transactions",
    )
    op.drop_index(
        "contract_internal_transactions_transaction_hash_idx",
        table_name="contract_internal_transactions",
    )
    op.drop_table("contract_internal_transactions")
    op.drop_index("blocks_timestamp_index", table_name="blocks")
    op.drop_index("blocks_number_index", table_name="blocks")
    op.drop_table("blocks")
    op.drop_index("block_ts_mapper_idx", table_name="block_ts_mapper")
    op.drop_table("block_ts_mapper")
    op.drop_table("address_token_balances")
    op.drop_table("address_coin_balances")
    # ### end Alembic commands ###
