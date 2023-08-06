from .snappicommon import SnappiList


class PortList(SnappiList):
    def __init__(self):
        super(PortList, self).__init__()


    def port(self, name=None, location=None):
        from .port import Port
        item = Port(name, location)
        self._add(item)
        return self
