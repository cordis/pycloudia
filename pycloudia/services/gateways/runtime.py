class Runtime(object):
    def __init__(self, client_id, facade_id, user_id=None):
        self.client_id = client_id
        self.facade_id = facade_id
        self.user_id = user_id
