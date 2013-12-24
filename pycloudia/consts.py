class NODE(object):
    class MODE(object):
        CONFIG = 'config'
        WORKER = 'worker'


class PACKAGE(object):
    class HEADER(object):
        class FORMAT(object):
            DELIMITER = ':'

        PEER = 'X-Peer-Identity'
        HOPS = 'X-Hops-Identity'
        REQUEST_ID = 'X-Request-Id'
        WORKER_ID = 'X-Worker-Id'
        TIMESTAMP = 'X-Timestamp'
        RESOURCE = 'X-Resource'
        CLUSTER = 'X-Cluster'
        CONFIG = 'X-Config'


class DISPATCHER(object):
    ANY = 'any'
    ALL = 'all'
