from .snappicommon import SnappiObject


class StateMetrics(SnappiObject):
    _TYPES = {
        'port_state': '.portstatelist.PortStateList',
        'flow_state': '.flowstatelist.FlowStateList',
    }

    def __init__(self):
        super(StateMetrics, self).__init__()

    @property
    def port_state(self):
        """port_state getter

        TBD

        Returns: list[obj(snappi.PortState)]
        """
        from .portstatelist import PortStateList
        if 'port_state' not in self._properties or self._properties['port_state'] is None:
            self._properties['port_state'] = PortStateList()
        return self._properties['port_state']

    @property
    def flow_state(self):
        """flow_state getter

        TBD

        Returns: list[obj(snappi.FlowState)]
        """
        from .flowstatelist import FlowStateList
        if 'flow_state' not in self._properties or self._properties['flow_state'] is None:
            self._properties['flow_state'] = FlowStateList()
        return self._properties['flow_state']
