from collections import defaultdict


class ConfigState(object):
    def __init__(self):
        self.workers_map = defaultdict(WorkerState)

    def update_worker_status(self, host, port, timestamp):
        worker_id = self._create_worker_id(host, port)
        worker = self._get_or_create_worker(worker_id)
        worker.set_timestamp(timestamp)
        worker.prolongate()

    def _create_worker_id(self, host, port):
        return ':'.join([host, port])

    def _get_or_create_worker(self, worker_id):
        return self.workers_map[worker_id]


class WorkerState(object):
    def __init__(self):
        self.timestamp = None

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def prolongate(self):
        pass
