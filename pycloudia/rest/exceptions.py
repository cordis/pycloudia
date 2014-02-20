class MissingArgumentError(LookupError):
    def __init__(self, argument, *args, **kwargs):
        self.argument = argument
        super(MissingArgumentError, self).__init__(*args, **kwargs)
