class Message(str):
    def __new__(cls, subject, peer=None, hops=None):
        instance = str.__new__(cls, subject)
        instance.peer = peer
        instance.hops = hops or []
        return instance
