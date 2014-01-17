class HEADER(object):
    REQUEST_ID = 'X-Request-Id'
    RESPONSE_ID = 'X-Response-Id'
    SOURCE_SERVICE = 'X-Source-Service'
    SOURCE_ADDRESS = 'X-Source-Identity'
    SOURCE_RUNTIME = 'X-Source-Decisive'
    TARGET_SERVICE = 'X-Target-Service'
    TARGET_RUNTIME = 'X-Target-Decisive'
    TARGET_ADDRESS = 'X-Target-Identity'
    STATUS = 'X-Status'
    REASON = 'X-Reason'


class STATUS(object):
    FAILURE = 'failure'
    SUCCESS = 'success'


class DEFAULT(object):
    REQUEST_TIMEOUT = 15
