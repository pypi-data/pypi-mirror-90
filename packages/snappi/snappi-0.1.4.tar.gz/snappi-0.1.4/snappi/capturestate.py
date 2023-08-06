from .snappicommon import SnappiObject


class CaptureState(SnappiObject):
    def __init__(self, port_names=None, state=None):
        super(CaptureState, self).__init__()
        self.port_names = port_names
        self.state = state

    @property
    def port_names(self):
        """port_names getter

        The name of ports to start capturing packets on. An empty or null list will control all port objects.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The name of ports to start capturing packets on. An empty or null list will control all port objects.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def state(self):
        """state getter

        The capture state.

        Returns: Union[start, stop]
        """
        return self._properties['state']

    @state.setter
    def state(self, value):
        """state setter

        The capture state.

        value: Union[start, stop]
        """
        self._properties['state'] = value
