from .snappicommon import SnappiList


class Layer1List(SnappiList):
    def __init__(self):
        super(Layer1List, self).__init__()


    def layer1(self, name=None, port_names=None, speed='speed_10_gbps', media='None', promiscuous=False, mtu=1500, ieee_media_defaults=True, auto_negotiate=True):
        from .layer1 import Layer1
        item = Layer1(name, port_names, speed, media, promiscuous, mtu, ieee_media_defaults, auto_negotiate)
        self._add(item)
        return self
