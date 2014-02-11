class Protocol(object):
    def listen(self, *args, **kwargs):
        pass


class ProtocolFactory(object):
    def __call__(self, director):
        """
        :type director: L{pycloudia.activities.facades.interfaces.IDirector}
        :rtype: L{pycloudia.activities.facades.tornado_impl.protocol.Protocol}
        """
        return Protocol()
