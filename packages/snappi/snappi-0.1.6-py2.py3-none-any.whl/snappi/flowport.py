from .snappicommon import SnappiObject


class FlowPort(SnappiObject):
    def __init__(self, tx_name=None, rx_name=None):
        super(FlowPort, self).__init__()
        self.tx_name = tx_name
        self.rx_name = rx_name

    @property
    def tx_name(self):
        """tx_name getter

        The unique name of a port that is the transmit port.

        Returns: str
        """
        return self._properties['tx_name']

    @tx_name.setter
    def tx_name(self, value):
        """tx_name setter

        The unique name of a port that is the transmit port.

        value: str
        """
        self._properties['tx_name'] = value

    @property
    def rx_name(self):
        """rx_name getter

        The unique name of a port that is the intended receive port.

        Returns: str
        """
        return self._properties['rx_name']

    @rx_name.setter
    def rx_name(self, value):
        """rx_name setter

        The unique name of a port that is the intended receive port.

        value: str
        """
        self._properties['rx_name'] = value
