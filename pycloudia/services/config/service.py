class ConfigService(object):
    worker_state_factory = None

    def __init__(self, runtime):
        self.runtime = runtime
        self.workers = {}

    def get_or_create_worker_id(self, identity):
        try:
            return self.workers[identity].get_id()
        except KeyError:
            worker = self.workers[identity] = self.worker_state_factory(identity)
            return worker.get_id()

    def init_worker(self, worker_id, host):
        self.workers[worker_id]

    def ping_worker(self, worker_id, timestamp):
        pass

    def add_replica(self, worker_id):
        pass


class WorkersRegistry(object):
    def __init__(self):
        self.workers_by_external_id = {}
        self.workers_by_internal_id = {}

    def get_by_external_id(self, external_id):
        return self.workers_by_external_id[external_id]

    def get_by_external_id(self, external_id):
        return self.workers_by_external_id[external_id]