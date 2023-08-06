from .snappicommon import SnappiList


class PortList(SnappiList):
    def __init__(self):
        super(PortList, self).__init__()


    def port(self, location=None, name=None):
        from .port import Port
        item = Port(location, name)
        self._add(item)
        return self
