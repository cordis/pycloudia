class UnicodeMessage(unicode):
    def __init__(self, subject, peer=None, hops=None):
        super(UnicodeMessage, self).__init__(subject)
        self.peer = peer
        self.hops = hops or []
