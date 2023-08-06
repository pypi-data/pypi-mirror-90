from .snappicommon import SnappiObject


class FlowDevice(SnappiObject):
    def __init__(self, tx_names=None, rx_names=None):
        super(FlowDevice, self).__init__()
        self.tx_names = tx_names
        self.rx_names = rx_names

    @property
    def tx_names(self):
        """tx_names getter

        The unique names of devices that will be transmitting.

        Returns: list[str]
        """
        return self._properties['tx_names']

    @tx_names.setter
    def tx_names(self, value):
        """tx_names setter

        The unique names of devices that will be transmitting.

        value: list[str]
        """
        self._properties['tx_names'] = value

    @property
    def rx_names(self):
        """rx_names getter

        The unique names of emulated devices that will be receiving.

        Returns: list[str]
        """
        return self._properties['rx_names']

    @rx_names.setter
    def rx_names(self, value):
        """rx_names setter

        The unique names of emulated devices that will be receiving.

        value: list[str]
        """
        self._properties['rx_names'] = value
