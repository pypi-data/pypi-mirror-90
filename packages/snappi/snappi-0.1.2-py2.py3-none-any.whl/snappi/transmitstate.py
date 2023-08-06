from .snappicommon import SnappiObject


class TransmitState(SnappiObject):
    def __init__(self, flow_names=None, state=None):
        super(TransmitState, self).__init__()
        self.flow_names = flow_names
        self.state = state

    @property
    def flow_names(self):
        """flow_names getter

        The names of flows to set transmit state on. If the list of flow_names is empty or null the state will be applied to all configured flows.

        Returns: list[str]
        """
        return self._properties['flow_names']

    @flow_names.setter
    def flow_names(self, value):
        """flow_names setter

        The names of flows to set transmit state on. If the list of flow_names is empty or null the state will be applied to all configured flows.

        value: list[str]
        """
        self._properties['flow_names'] = value

    @property
    def state(self):
        """state getter

        The transmit state.

        Returns: Union[start, stop, pause]
        """
        return self._properties['state']

    @state.setter
    def state(self, value):
        """state setter

        The transmit state.

        value: Union[start, stop, pause]
        """
        self._properties['state'] = value
