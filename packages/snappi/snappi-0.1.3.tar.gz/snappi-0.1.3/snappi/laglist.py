from .snappicommon import SnappiList


class LagList(SnappiList):
    def __init__(self):
        super(LagList, self).__init__()


    def lag(self, name=None, port_names=None):
        from .lag import Lag
        item = Lag(name, port_names)
        self._add(item)
        return self
