from .snappicommon import SnappiList


class FlowBitPatternList(SnappiList):
    def __init__(self):
        super(FlowBitPatternList, self).__init__()


    def flowbitpattern(self):
        from .flowbitpattern import FlowBitPattern
        item = FlowBitPattern()
        self._add(item)
        return self

    def bitlist(self, offset=1, length=1, count=1, values=None):
        from .flowbitpattern import FlowBitPattern
        item = FlowBitPattern()
        item.bitlist
        self._add(item)
        return self

    def bitcounter(self, offset=0, length=32, count=1, start=0, step=0):
        from .flowbitpattern import FlowBitPattern
        item = FlowBitPattern()
        item.bitcounter
        self._add(item)
        return self
