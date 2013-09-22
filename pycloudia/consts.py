class NODE(object):
    class MODE(object):
        CONFIG = 'config'
        WORKER = 'worker'


class PACKAGE(object):
    ENCODING = 'utf8'
    DELIMITER = '\r\n\r\n'

    class HEADER(object):
        RESOURCE = 'X-Resource'
        WORKER_ID = 'X-Worker-Id'
        TIMESTAMP = 'X-Timestamp'
