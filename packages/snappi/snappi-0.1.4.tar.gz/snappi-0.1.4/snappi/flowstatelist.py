from .snappicommon import SnappiList


class FlowStateList(SnappiList):
    def __init__(self):
        super(FlowStateList, self).__init__()


    def state(self, name=None, transmit='None'):
        from .flowstate import FlowState
        item = FlowState(name, transmit)
        self._add(item)
        return self
