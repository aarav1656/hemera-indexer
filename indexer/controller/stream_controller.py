import logging
import os
import time

import mpire

from common.utils.exception_control import FastShutdownError, HemeraBaseException
from common.utils.file_utils import delete_file, write_to_file
from common.utils.web3_utils import build_web3
from indexer.controller.base_controller import BaseController
from indexer.controller.scheduler.job_scheduler import JobScheduler
from indexer.utils.limit_reader import LimitReader
from indexer.utils.sync_recorder import BaseRecorder

logger = logging.getLogger(__name__)


class StreamController(BaseController):

    def __init__(
        self,
        batch_web3_provider,
        sync_recorder: BaseRecorder,
        job_scheduler: JobScheduler,
        limit_reader: LimitReader,
        max_retries=5,
        retry_from_record=False,
        delay=0,
        process_numbers=1,
        process_size=None,
        process_time_out=None,
    ):
        self.entity_types = 1
        self.web3 = build_web3(batch_web3_provider)
        self.sync_recorder = sync_recorder
        self.job_scheduler = job_scheduler
        self.limit_reader = limit_reader
        self.max_retries = max_retries
        self.retry_from_record = retry_from_record
        self.delay = delay

        self.process_numbers = process_numbers
        self.process_size = process_size
        self.process_time_out = process_time_out
        if self.process_numbers <= 1:
            self.pool = None
        else:
            self.pool = mpire.WorkerPool(n_jobs=self.process_numbers, use_dill=True, keep_alive=True)

    def action(
        self,
        start_block=None,
        end_block=None,
        block_batch_size=10,
        period_seconds=10,
        retry_errors=True,
        pid_file=None,
    ):
        try:
            if pid_file is not None:
                logger.info("Creating pid file {}".format(pid_file))
                write_to_file(pid_file, str(os.getpid()))

            last_synced_block = self.sync_recorder.get_last_synced_block()

            if start_block is not None:
                if (
                    not self.retry_from_record
                    or last_synced_block < start_block
                    or (end_block is not None and last_synced_block > end_block)
                ):
                    last_synced_block = start_block - 1

            while True and (end_block is None or last_synced_block < end_block):
                synced_blocks = 0

                current_block = self.limit_reader.get_current_block_number()
                if current_block is None:
                    raise FastShutdownError(
                        "Can't get current limit block number from limit reader."
                        "If you're using PGLimitReader, please confirm blocks table has one record at least."
                    )

                target_block = self._calculate_target_block(
                    current_block, last_synced_block, end_block, block_batch_size
                )
                synced_blocks = max(target_block - last_synced_block, 0)

                logger.info(
                    "Current block {}, target block {}, last synced block {}, blocks to sync {}".format(
                        current_block, target_block, last_synced_block, synced_blocks
                    )
                )

                if synced_blocks != 0:
                    if not self.pool:
                        self._do_stream(last_synced_block + 1, target_block)
                    else:
                        splits = self.split_blocks(last_synced_block + 1, target_block, self.process_size)
                        self.pool.map(func=self._do_stream, iterable_of_args=splits, task_timeout=self.process_time_out)
                    logger.info("Writing last synced block {}".format(target_block))
                    self.sync_recorder.set_last_synced_block(target_block)
                    last_synced_block = target_block

                if synced_blocks <= 0:
                    logger.info("Nothing to sync. Sleeping for {} seconds...".format(period_seconds))
                    time.sleep(period_seconds)

        finally:
            if pid_file is not None:
                logger.info("Deleting pid file {}".format(pid_file))
                delete_file(pid_file)

    def _shutdown(self):
        pass

    def split_blocks(self, start_block, end_block, step):
        blocks = []
        for i in range(start_block, end_block + 1, step):
            blocks.append((i, min(i + step - 1, end_block)))
        return blocks

    def _do_stream(self, start_block, end_block):

        for retry in range(self.max_retries + 1):
            try:
                # ETL program's main logic
                self.job_scheduler.run_jobs(start_block, end_block)
                return

            except HemeraBaseException as e:
                logger.error(f"An expected exception occurred while syncing block data. error: {e}")
                if e.crashable:
                    logger.error("Mission will crash immediately.")
                    raise e

                if e.retriable:
                    if retry == self.max_retries:
                        logger.info(f"The number of retry is reached limit {self.max_retries}.")
                    else:
                        logger.info(f"No: {retry} retry is about to start.")
                else:
                    logger.error("Mission will not retry, and exit immediately.")
                    raise e

            except Exception as e:
                logger.error(f"An unknown exception occurred while syncing block data. error: {e}")
                raise e

        logger.error(
            f"The job with parameters start_block:{start_block}, end_block:{end_block} "
            f"can't be automatically resumed after reached out limit of retries. Program will exit."
        )

    def _get_current_block_number(self):
        return int(self.web3.eth.block_number)

    def _calculate_target_block(self, current_block, last_synced_block, end_block, steps):
        target_block = min(current_block - self.delay, last_synced_block + steps)
        target_block = min(target_block, end_block) if end_block is not None else target_block
        return target_block

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.pool.terminate()
        except Exception:
            pass
