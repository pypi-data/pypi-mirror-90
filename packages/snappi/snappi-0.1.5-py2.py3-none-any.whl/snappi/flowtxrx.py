from .snappicommon import SnappiObject


class FlowTxRx(SnappiObject):
    _TYPES = {
        'port': '.flowport.FlowPort',
        'device': '.flowdevice.FlowDevice',
    }

    def __init__(self):
        super(FlowTxRx, self).__init__()

    @property
    def port(self):
        from .flowport import FlowPort
        if 'port' not in self._properties or self._properties['port'] is None:
            self._properties['port'] = FlowPort()
        self.choice = 'port'
        return self._properties['port']

    @property
    def device(self):
        from .flowdevice import FlowDevice
        if 'device' not in self._properties or self._properties['device'] is None:
            self._properties['device'] = FlowDevice()
        self.choice = 'device'
        return self._properties['device']

    @property
    def choice(self):
        """choice getter

        The type of transmit and receive container used by the flow.

        Returns: Union[port, device, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of transmit and receive container used by the flow.

        value: Union[port, device, choice, choice, choice]
        """
        self._properties['choice'] = value
