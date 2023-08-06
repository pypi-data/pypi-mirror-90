from .snappicommon import SnappiList


class PortStateList(SnappiList):
    def __init__(self):
        super(PortStateList, self).__init__()


    def portstate(self, name=None, link='None', capture='None'):
        from .portstate import PortState
        item = PortState(name, link, capture)
        self._add(item)
        return self
