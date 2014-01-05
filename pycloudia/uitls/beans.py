class DataBean(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '%s<%r>' % (
            self.__class__.__name__,
            self.__dict__
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
