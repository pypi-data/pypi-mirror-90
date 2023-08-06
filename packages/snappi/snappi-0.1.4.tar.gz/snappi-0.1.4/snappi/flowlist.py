from .snappicommon import SnappiList


class FlowList(SnappiList):
    def __init__(self):
        super(FlowList, self).__init__()


    def flow(self, name=None):
        from .flow import Flow
        item = Flow(name)
        self._add(item)
        return self
