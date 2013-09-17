class ConfigState(object):
    def __init__(self, clusters_config, channels_config, services_config):
        self.clusters_config = clusters_config
        self.channels_config = channels_config
        self.services_config = services_config
        self.clusters = self._create_clusters(clusters_config.clusters)
        self.configs = self._create_configs(clusters_config.configs)

    def _create_clusters(self, clusters):
        pass

    def _create_configs(self, configs):
        pass

    def register_worker(self, cluster_name, host):
        cluster = self.clusters[cluster_name]
        machine = cluster.get_or_create_machine_by_host(host)
        worker = machine.get_or_create_worker()
        worker.set_online()


class ClusterState(object):
    def __init__(self):
        self.machines = {}


class MachineState(object):
    def __init__(self):
        self.workers = {}


class WorkerState(object):
    def __init__(self):
        self.services = {}


class ServiceState(object):
    def __init__(self):
        pass
