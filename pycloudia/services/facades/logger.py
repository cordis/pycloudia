class Logger(object):
    def __init__(self, subject):
        self.subject = subject

    def log_client_not_found(self, client_id):
        self.subject.warn('Client `%s` not found', client_id)

    def log_header_not_found(self, header_name):
        self.subject.warn('Header `%s` not found', header_name)
