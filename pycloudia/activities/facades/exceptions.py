class ListenFailedError(Exception):
    def __init__(self, host, port, *args, **kwargs):
        self.host = host
        self.port = port
        super(ListenFailedError, self).__init__(*args, **kwargs)

    def __str__(self):
        return 'Listening failed on {0}:{1}'.format(self.host, self.port)
