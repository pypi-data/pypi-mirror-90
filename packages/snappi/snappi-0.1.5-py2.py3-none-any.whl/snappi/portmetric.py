from .snappicommon import SnappiObject


class PortMetric(SnappiObject):
    def __init__(self, name=None, location=None, link=None, capture=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, bytes_tx_rate=None, bytes_rx_rate=None):
        super(PortMetric, self).__init__()
        self.name = name
        self.location = location
        self.link = link
        self.capture = capture
        self.frames_tx = frames_tx
        self.frames_rx = frames_rx
        self.bytes_tx = bytes_tx
        self.bytes_rx = bytes_rx
        self.frames_tx_rate = frames_tx_rate
        self.frames_rx_rate = frames_rx_rate
        self.bytes_tx_rate = bytes_tx_rate
        self.bytes_rx_rate = bytes_rx_rate

    @property
    def name(self):
        """name getter

        The name of a configured port

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured port

        value: str
        """
        self._properties['name'] = value

    @property
    def location(self):
        """location getter

        The state of the connection to the test port location. The format should be the configured port location along with any custom connection state message.

        Returns: str
        """
        return self._properties['location']

    @location.setter
    def location(self, value):
        """location setter

        The state of the connection to the test port location. The format should be the configured port location along with any custom connection state message.

        value: str
        """
        self._properties['location'] = value

    @property
    def link(self):
        """link getter

        The state of the test port link The string can be up, down or a custom error message.

        Returns: Union[up, down]
        """
        return self._properties['link']

    @link.setter
    def link(self, value):
        """link setter

        The state of the test port link The string can be up, down or a custom error message.

        value: Union[up, down]
        """
        self._properties['link'] = value

    @property
    def capture(self):
        """capture getter

        The state of the test port capture infrastructure. The string can be started, stopped or a custom error message.

        Returns: Union[started, stopped]
        """
        return self._properties['capture']

    @capture.setter
    def capture(self, value):
        """capture setter

        The state of the test port capture infrastructure. The string can be started, stopped or a custom error message.

        value: Union[started, stopped]
        """
        self._properties['capture'] = value

    @property
    def frames_tx(self):
        """frames_tx getter

        The current total number of frames transmitted

        Returns: int
        """
        return self._properties['frames_tx']

    @frames_tx.setter
    def frames_tx(self, value):
        """frames_tx setter

        The current total number of frames transmitted

        value: int
        """
        self._properties['frames_tx'] = value

    @property
    def frames_rx(self):
        """frames_rx getter

        The current total number of valid frames received

        Returns: int
        """
        return self._properties['frames_rx']

    @frames_rx.setter
    def frames_rx(self, value):
        """frames_rx setter

        The current total number of valid frames received

        value: int
        """
        self._properties['frames_rx'] = value

    @property
    def bytes_tx(self):
        """bytes_tx getter

        The current total number of bytes transmitted

        Returns: int
        """
        return self._properties['bytes_tx']

    @bytes_tx.setter
    def bytes_tx(self, value):
        """bytes_tx setter

        The current total number of bytes transmitted

        value: int
        """
        self._properties['bytes_tx'] = value

    @property
    def bytes_rx(self):
        """bytes_rx getter

        The current total number of valid bytes received

        Returns: int
        """
        return self._properties['bytes_rx']

    @bytes_rx.setter
    def bytes_rx(self, value):
        """bytes_rx setter

        The current total number of valid bytes received

        value: int
        """
        self._properties['bytes_rx'] = value

    @property
    def frames_tx_rate(self):
        """frames_tx_rate getter

        The current rate of frames transmitted

        Returns: float
        """
        return self._properties['frames_tx_rate']

    @frames_tx_rate.setter
    def frames_tx_rate(self, value):
        """frames_tx_rate setter

        The current rate of frames transmitted

        value: float
        """
        self._properties['frames_tx_rate'] = value

    @property
    def frames_rx_rate(self):
        """frames_rx_rate getter

        The current rate of valid frames received

        Returns: float
        """
        return self._properties['frames_rx_rate']

    @frames_rx_rate.setter
    def frames_rx_rate(self, value):
        """frames_rx_rate setter

        The current rate of valid frames received

        value: float
        """
        self._properties['frames_rx_rate'] = value

    @property
    def bytes_tx_rate(self):
        """bytes_tx_rate getter

        The current rate of bytes transmitted

        Returns: float
        """
        return self._properties['bytes_tx_rate']

    @bytes_tx_rate.setter
    def bytes_tx_rate(self, value):
        """bytes_tx_rate setter

        The current rate of bytes transmitted

        value: float
        """
        self._properties['bytes_tx_rate'] = value

    @property
    def bytes_rx_rate(self):
        """bytes_rx_rate getter

        The current rate of bytes received

        Returns: float
        """
        return self._properties['bytes_rx_rate']

    @bytes_rx_rate.setter
    def bytes_rx_rate(self, value):
        """bytes_rx_rate setter

        The current rate of bytes received

        value: float
        """
        self._properties['bytes_rx_rate'] = value
