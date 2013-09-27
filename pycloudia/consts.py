class NODE(object):
    class MODE(object):
        CONFIG = 'config'
        WORKER = 'worker'


class PACKAGE(object):
    ENCODING = 'utf8'
    DELIMITER = '\r\n\r\n'

    class HEADER(object):
        class FORMAT(object):
            DELIMITER = ':'

        RESOURCE = 'X-Resource'
        WORKER_ID = 'X-Worker-Id'
        TIMESTAMP = 'X-Timestamp'
        CLUSTER = 'X-Cluster'


class DISPATCHER(object):
    ANY = 'any'
    ALL = 'all'
