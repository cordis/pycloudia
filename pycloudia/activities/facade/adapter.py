from functools import partial

from pycloudia.activities.clients.consts import HEADER


class ActivityAdapter(object):
    encoder = None
    decoder = None

    def __init__(self, subject):
        self.subject = subject

    def connection_made(self, client_id, send_func):
        self.subject.create_client_activity(client_id, partial(self.send_package, send_func))

    def connection_lost(self, client_id, reason):
        self.subject.delete_client_activity(client_id, reason)

    def connection_done(self, client_id):
        self.subject.delete_client_activity(client_id)

    def read_message(self, client_id, message):
        package = self.decoder.decode(message)
        package.set_header(HEADER.CLIENT_ID, client_id)
        self.subject.process_incoming_package(package)

    def send_package(self, send_func, package):
        package.del_header(HEADER.CLIENT_ID)
        message = self.encoder.encode(package)
        send_func(message)
