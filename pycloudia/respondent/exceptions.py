class ResponseError(RuntimeError):
    def __init__(self, request_id, *args, **kwargs):
        self.request_id = request_id
        super(ResponseError, self).__init__(*args, **kwargs)


class ResponseTimeoutError(ResponseError):
    pass


class ResponseNotHandledError(ResponseError):
    pass
