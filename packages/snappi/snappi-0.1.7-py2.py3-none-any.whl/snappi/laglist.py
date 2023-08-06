from .snappicommon import SnappiList


class LagList(SnappiList):
    def __init__(self):
        super(LagList, self).__init__()


    def lag(self, port_names=None, name=None):
        from .lag import Lag
        item = Lag(port_names, name)
        self._add(item)
        return self
