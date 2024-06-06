import json

from domain.log import format_log_data
from domain.transaction import format_transaction_data
from exporters.console_item_exporter import ConsoleItemExporter
from jobs.base_job import BaseJob
from executors.batch_work_executor import BatchWorkExecutor
from utils.enrich import enrich_blocks_timestamp, enrich_transactions
from utils.json_rpc_requests import generate_get_receipt_json_rpc
from utils.utils import rpc_response_batch_to_results


# Exports transactions and logs
class ExportTransactionsAndLogsJob(BaseJob):
    def __init__(self,
                 index_keys,
                 batch_web3_provider,
                 batch_size,
                 max_workers,
                 item_exporter=ConsoleItemExporter()):
        super().__init__(index_keys)
        self._batch_web3_provider = batch_web3_provider
        self._transaction_hashes_iterable = (transaction['hash'] for transaction in self._data_buff['transaction'])
        self._batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self._item_exporter = item_exporter

    def _start(self):
        super()._start()

    def _collect(self):
        self._batch_work_executor.execute(self._transaction_hashes_iterable, self._collect_batch)

    def _collect_batch(self, transaction_hashes):
        receipts_rpc = list(generate_get_receipt_json_rpc(transaction_hashes))
        response = self._batch_web3_provider.make_batch_request(json.dumps(receipts_rpc))
        results = rpc_response_batch_to_results(response)
        for receipt in results:
            receipt['item'] = 'receipt'
            self._collect_item(receipt)
            for log in receipt['logs']:
                log['item'] = 'log'
                self._collect_item(log)

    def _process(self):
        self._data_buff['enriched_transaction'] = [format_transaction_data(transaction)
                                                   for transaction in enrich_blocks_timestamp
                                                   (self._data_buff['block'],
                                                    enrich_transactions(self._data_buff['transaction'],
                                                                        self._data_buff['receipt']))]

        self._data_buff['enriched_log'] = [format_log_data(log) for log in
                                           enrich_blocks_timestamp(self._data_buff['block'],
                                                                   self._data_buff['log'])]

        self._data_buff['enriched_transaction'] = sorted(self._data_buff['enriched_transaction'],
                                                         key=lambda x: (x['block_number'],
                                                                        x['transaction_index']))

        self._data_buff['enriched_log'] = sorted(self._data_buff['enriched_log'],
                                                 key=lambda x: (x['block_number'],
                                                                x['transaction_index'],
                                                                x['log_index']))

    def _export(self):
        items = self._extract_from_buff(['enriched_transaction', 'enriched_log'])
        self._item_exporter.export_items(items)

    def _end(self):
        self._batch_work_executor.shutdown()
        super()._end()
