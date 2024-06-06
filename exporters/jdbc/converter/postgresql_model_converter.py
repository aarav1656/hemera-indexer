from datetime import timezone, datetime

from sqlalchemy import func


class PostgreSQLModelConverter:

    def __init__(self, confirm):
        self.confirm = confirm

    def convert_item(self, table, data):

        if table == "blocks":
            return self.convert_to_block(data)

        elif table == "transactions":
            return self.convert_to_transaction(data)

        elif table == "logs":
            return self.convert_to_log(data)

        elif table == "traces":
            return self.convert_to_trace(data)

        elif table == "contract_internal_transactions":
            return self.convert_to_contract_internal_transactions(data)

        elif table == "contracts":
            return self.convert_to_contract(data)

        elif table == "address_coin_balances":
            return self.convert_to_coin_balance(data)

        elif table == "erc20_token_transfers":
            return self.convert_to_erc20_token_transfer(data)

        elif table == "erc20_token_holders":
            return self.convert_to_erc20_token_holder(data)

        elif table == "erc721_token_transfers":
            return self.convert_to_erc721_token_transfer(data)

        elif table == "erc721_token_holders":
            return self.convert_to_erc721_token_holder(data)

        elif table == "erc1155_token_transfers":
            return self.convert_to_erc1155_token_transfer(data)

        elif table == "erc1155_token_holders":
            return self.convert_to_erc1155_token_holder(data)

        elif table == "tokens":
            return self.convert_to_tokens(data)

        elif table == "address_token_balances":
            return self.convert_to_token_balance(data)

        elif table == "block_ts_mapper":
            return self.convert_to_block_ts_mapper(data)

        else:
            return None

    def convert_to_block(self, block):
        return {
            'hash': bytes(block["hash"], 'utf-8'),
            'number': block["number"],
            'timestamp': func.to_timestamp(block["timestamp"]),
            'parent_hash': bytes(block["parent_hash"], 'utf-8'),
            'nonce': bytes(block["nonce"], 'utf-8'),
            'gas_limit': block["gas_limit"],
            'gas_used': block["gas_used"],
            'base_fee_per_gas': block["base_fee_per_gas"],
            'difficulty': block["difficulty"],
            'size': block["size"],
            'miner': bytes(block["miner"], 'utf-8'),
            'sha3_uncles': bytes(block["sha3_uncles"], 'utf-8'),
            'transactions_root': bytes(block["transactions_root"], 'utf-8'),
            'transactions_count': block["transactions_count"],
            'state_root': bytes(block["state_root"], 'utf-8'),
            'receipts_root': bytes(block["receipts_root"], 'utf-8'),
            'extra_data': bytes(block["extra_data"], 'utf-8'),
            'withdrawals_root': bytes(block["withdrawals_root"], 'utf-8') if block["withdrawals_root"] else None,
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_transaction(self, transaction):
        return {
            'hash': bytes(transaction["hash"], 'utf-8'),
            'transaction_index': transaction["transaction_index"],
            'from_address': bytes(transaction["from_address"], 'utf-8') if transaction["from_address"] else None,
            'to_address': bytes(transaction["to_address"], 'utf-8') if transaction["to_address"] else None,
            'value': transaction["value"],
            'transaction_type': transaction["transaction_type"],
            'input': bytes(transaction["input"], 'utf-8'),
            'nonce': transaction["nonce"],
            'block_hash': bytes(transaction["block_hash"], 'utf-8'),
            'block_number': transaction["block_number"],
            'block_timestamp': func.to_timestamp(transaction["block_timestamp"]),
            'gas': transaction["gas"],
            'gas_price': transaction["gas_price"],
            'max_fee_per_gas': transaction["max_fee_per_gas"],
            'max_priority_fee_per_gas': transaction["max_priority_fee_per_gas"],
            'receipt_root': bytes(transaction["receipt_root"], 'utf-8') if transaction["receipt_root"] else None,
            'receipt_status': transaction["receipt_status"],
            'receipt_gas_used': transaction["receipt_gas_used"],
            'receipt_cumulative_gas_used': transaction["receipt_cumulative_gas_used"],
            'receipt_effective_gas_price': transaction["receipt_effective_gas_price"],
            'receipt_l1_fee': transaction["receipt_l1_fee"],
            'receipt_l1_fee_scalar': transaction["receipt_l1_fee_scalar"],
            'receipt_l1_gas_used': transaction["receipt_l1_gas_used"],
            'receipt_l1_gas_price': transaction["receipt_l1_gas_price"],
            'blob_versioned_hashes': [bytes(_, 'utf-8') for _ in transaction["blob_versioned_hashes"]] \
                if transaction["blob_versioned_hashes"] else None,
            'receipt_contract_address': bytes(transaction["receipt_contract_address"],
                                              'utf-8') if transaction["receipt_contract_address"] else None,
            'exist_error': transaction["exist_error"],
            'error': transaction["error"],
            'revert_reason': transaction["revert_reason"],
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_log(self, log):
        return {
            'log_index': log["log_index"],
            'address': bytes(log["address"], 'utf-8'),
            'data': bytes(log["data"], 'utf-8'),
            'topic0': bytes(log["topic0"], 'utf-8'),
            'topic1': bytes(log["topic1"], 'utf-8') if log["topic1"] else None,
            'topic2': bytes(log["topic2"], 'utf-8') if log["topic2"] else None,
            'topic3': bytes(log["topic3"], 'utf-8') if log["topic3"] else None,
            'transaction_hash': bytes(log["transaction_hash"], 'utf-8'),
            'transaction_index': log["transaction_index"],
            'block_number': log["block_number"],
            'block_hash': bytes(log["block_hash"], 'utf-8'),
            'block_timestamp': func.to_timestamp(log["block_timestamp"]),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_trace(self, trace):
        return {
            "trace_id": trace["trace_id"],
            "from_address": bytes(trace["from_address"], 'utf-8') if trace["from_address"] else None,
            "to_address": bytes(trace["to_address"], 'utf-8') if trace["to_address"] else None,
            "value": trace["value"],
            "input": bytes(trace["input"], 'utf-8') if trace["input"] else None,
            "output": bytes(trace["output"], 'utf-8') if trace["output"] else None,
            "trace_type": trace["trace_type"],
            "call_type": trace["call_type"],
            "gas": trace["gas"],
            "gas_used": trace["gas_used"],
            "subtraces": trace["subtraces"],
            "trace_address": trace["trace_address"],
            "error": trace["error"],
            "status": trace["status"],
            'block_number': trace["block_number"],
            'block_hash': bytes(trace["block_hash"], 'utf-8') if trace["block_hash"] else None,
            'block_timestamp': func.to_timestamp(trace["block_timestamp"]),
            'transaction_index': trace["transaction_index"],
            'transaction_hash': bytes(trace["transaction_hash"], 'utf-8') if trace["transaction_hash"] else None,
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_contract_internal_transactions(self, internal_transactions):
        return {
            "trace_id": internal_transactions["trace_id"],
            "from_address": bytes(internal_transactions["from_address"], 'utf-8') if internal_transactions[
                "from_address"] else None,
            "to_address": bytes(internal_transactions["to_address"], 'utf-8') if internal_transactions[
                "to_address"] else None,
            "value": internal_transactions["value"],
            "trace_type": internal_transactions["trace_type"],
            "call_type": internal_transactions["call_type"],
            "gas": internal_transactions["gas"],
            "gas_used": internal_transactions["gas_used"],
            "trace_address": internal_transactions["trace_address"],
            "error": internal_transactions["error"],
            "status": internal_transactions["status"],
            'block_number': internal_transactions["block_number"],
            'block_hash': bytes(internal_transactions["block_hash"], 'utf-8') if internal_transactions[
                "block_hash"] else None,
            'block_timestamp': func.to_timestamp(internal_transactions["block_timestamp"]),
            'transaction_index': internal_transactions["transaction_index"],
            'transaction_hash': bytes(internal_transactions["transaction_hash"], 'utf-8') if internal_transactions[
                "transaction_hash"] else None,
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_contract(self, contract):
        return {
            'address': bytes(contract['address'], 'utf-8'),
            'name': contract['name'],
            'contract_creator': bytes(contract['contract_creator'], 'utf-8'),
            'creation_code': bytes(contract['creation_code'], 'utf-8'),
            'deployed_code': bytes(contract['deployed_code'], 'utf-8'),
            'block_number': contract['block_number'],
            'block_hash': bytes(contract['block_hash'], 'utf-8'),
            'block_timestamp': func.to_timestamp(contract["block_timestamp"]),
            'transaction_index': contract['transaction_index'],
            'transaction_hash': bytes(contract['transaction_hash'], 'utf-8'),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_coin_balance(self, coin_balance):
        return {
            'address': bytes(coin_balance['address'], 'utf-8'),
            'balance': coin_balance['balance'],
            'block_number': coin_balance["block_number"],
            'block_timestamp': func.to_timestamp(coin_balance["block_timestamp"]),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_erc20_token_transfer(self, token_transfer):
        return {
            'transaction_hash': bytes(token_transfer["transaction_hash"], 'utf-8'),
            'log_index': token_transfer["log_index"],
            "from_address": bytes(token_transfer["from_address"], 'utf-8'),
            "to_address": bytes(token_transfer["to_address"], 'utf-8'),
            "token_address": bytes(token_transfer["token_address"], 'utf-8'),
            "value": token_transfer["value"],
            'block_number': token_transfer["block_number"],
            'block_hash': bytes(token_transfer["block_hash"], 'utf-8'),
            'block_timestamp': func.to_timestamp(token_transfer["block_timestamp"]),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_erc20_token_holder(self, token_holder):
        return {
            "token_address": bytes(token_holder["token_address"], 'utf-8'),
            "wallet_address": bytes(token_holder["wallet_address"], 'utf-8'),
            "balance_of": token_holder["balance_of"],
            'block_number': token_holder["block_number"],
            'block_timestamp': func.to_timestamp(token_holder["block_timestamp"]),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_erc721_token_transfer(self, token_transfer):
        return {
            'transaction_hash': bytes(token_transfer["transaction_hash"], 'utf-8'),
            'log_index': token_transfer["log_index"],
            "from_address": bytes(token_transfer["from_address"], 'utf-8'),
            "to_address": bytes(token_transfer["to_address"], 'utf-8'),
            "token_address": bytes(token_transfer["token_address"], 'utf-8'),
            "token_id": token_transfer["token_id"],
            'block_number': token_transfer["block_number"],
            'block_hash': bytes(token_transfer["block_hash"], 'utf-8'),
            'block_timestamp': func.to_timestamp(token_transfer["block_timestamp"]),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_erc721_token_holder(self, token_holder):
        return {
            "token_address": bytes(token_holder["token_address"], 'utf-8'),
            "wallet_address": bytes(token_holder["wallet_address"], 'utf-8'),
            "balance_of": token_holder["balance_of"],
            'block_number': token_holder["block_number"],
            'block_timestamp': func.to_timestamp(token_holder["block_timestamp"]),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_erc1155_token_transfer(self, token_transfer):
        return {
            'transaction_hash': bytes(token_transfer["transaction_hash"], 'utf-8'),
            'log_index': token_transfer["log_index"],
            "from_address": bytes(token_transfer["from_address"], 'utf-8'),
            "to_address": bytes(token_transfer["to_address"], 'utf-8'),
            "token_address": bytes(token_transfer["token_address"], 'utf-8'),
            "token_id": token_transfer["token_id"],
            "value": token_transfer["value"],
            'block_number': token_transfer["block_number"],
            'block_hash': bytes(token_transfer["block_hash"], 'utf-8'),
            'block_timestamp': func.to_timestamp(token_transfer["block_timestamp"]),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_erc1155_token_holder(self, token_holder):
        return {
            "token_address": bytes(token_holder["token_address"], 'utf-8'),
            "wallet_address": bytes(token_holder["wallet_address"], 'utf-8'),
            "token_id": token_holder["token_id"],
            "balance_of": token_holder["balance_of"],
            "last_call_contract_time": func.to_timestamp(token_holder["last_call_contract_time"]),
            'block_number': token_holder["block_number"],
            'block_timestamp': func.to_timestamp(token_holder["block_timestamp"]),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_tokens(self, token):
        return {
            "address": bytes(token["address"], 'utf-8'),
            'name': token['name'],
            'symbol': token['symbol'],
            'total_supply': token['total_supply'],
            'decimals': token['decimals'],
            'token_type': token['token_type'],
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_token_balance(self, token_balance):
        return {
            'address': bytes(token_balance["address"], 'utf-8'),
            "token_id": token_balance["token_id"],
            "token_type": token_balance["token_type"],
            "token_address": bytes(token_balance["token_address"], 'utf-8'),
            "balance": token_balance["balance"],
            'block_number': token_balance["block_number"],
            'block_timestamp': func.to_timestamp(token_balance["block_timestamp"]),
            'update_time': func.to_timestamp(int(datetime.now(timezone.utc).timestamp())) if self.confirm else None,
        }

    def convert_to_block_ts_mapper(self, mapper):
        return {
            "ts": mapper["timestamp"],
            "block_number": mapper["block_number"],
            "timestamp": func.to_timestamp(mapper["timestamp"]),
        }
