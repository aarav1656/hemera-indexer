import json

from domain.block import format_block_data
from domain.block_ts_mapper import format_block_ts_mapper
from executors.batch_work_executor import BatchWorkExecutor
from exporters.console_item_exporter import ConsoleItemExporter
from jobs.base_job import BaseJob
from utils.json_rpc_requests import generate_get_block_by_number_json_rpc
from utils.utils import rpc_response_batch_to_results, validate_range


# Exports blocks and block number <-> timestamp mapping
class ExportBlocksJob(BaseJob):
    def __init__(self,
                 index_keys,
                 start_block,
                 end_block,
                 batch_web3_provider,
                 batch_size,
                 max_workers,
                 item_exporter=ConsoleItemExporter()):
        super().__init__(index_keys)
        validate_range(start_block, end_block)
        self._start_block = start_block
        self._end_block = end_block
        self._batch_web3_provider = batch_web3_provider
        self._batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self._item_exporter = item_exporter

    def _start(self):
        super()._start()

    def _collect(self):
        self._batch_work_executor.execute(
            range(self._start_block, self._end_block + 1),
            self._collect_batch,
            total_items=self._end_block - self._start_block + 1
        )

    def _collect_batch(self, block_number_batch):
        blocks_rpc = list(generate_get_block_by_number_json_rpc(block_number_batch, True))
        response = self._batch_web3_provider.make_batch_request(json.dumps(blocks_rpc))
        results = rpc_response_batch_to_results(response)

        for block in results:
            block['item'] = 'block'
            self._collect_item(block)
            for transaction in block['transactions']:
                transaction['item'] = 'transaction'
                self._collect_item(transaction)

    def _process(self):
        self._data_buff['formated_block'] = [format_block_data(block) for block in self._data_buff['block']]
        self._data_buff['formated_block'] = sorted(self._data_buff['formated_block'], key=lambda x: x['number'])

        ts_dict = {}
        for block in self._data_buff['formated_block']:
            timestamp = int(block['timestamp'] / 3600) * 3600
            block_number = block['number']

            if timestamp not in ts_dict.keys() or block_number < ts_dict[timestamp]:
                ts_dict[timestamp] = block_number
        self._data_buff['block_ts_mapping'] = []
        for timestamp, block_number in ts_dict.items():
            self._data_buff['block_ts_mapping'].append(format_block_ts_mapper(timestamp, block_number))

    def _export(self):
        export_items = self._extract_from_buff(['formated_block', 'block_ts_mapping'])
        self._item_exporter.export_items(export_items)

    def _end(self):
        self._batch_work_executor.shutdown()
        super()._end()
