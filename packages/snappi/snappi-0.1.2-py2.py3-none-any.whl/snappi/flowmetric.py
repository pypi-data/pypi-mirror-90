from .snappicommon import SnappiObject


class FlowMetric(SnappiObject):
    def __init__(self, name=None, transmit=None, port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, loss=None, additionalProperties=None):
        super(FlowMetric, self).__init__()
        self.name = name
        self.transmit = transmit
        self.port_tx = port_tx
        self.port_rx = port_rx
        self.frames_tx = frames_tx
        self.frames_rx = frames_rx
        self.bytes_tx = bytes_tx
        self.bytes_rx = bytes_rx
        self.frames_tx_rate = frames_tx_rate
        self.frames_rx_rate = frames_rx_rate
        self.loss = loss
        self.additionalProperties = additionalProperties

    @property
    def name(self):
        """name getter

        The name of a configured flow.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured flow.

        value: str
        """
        self._properties['name'] = value

    @property
    def transmit(self):
        """transmit getter

        The transmit state of the flow.

        Returns: Union[started, stopped, paused]
        """
        return self._properties['transmit']

    @transmit.setter
    def transmit(self, value):
        """transmit setter

        The transmit state of the flow.

        value: Union[started, stopped, paused]
        """
        self._properties['transmit'] = value

    @property
    def port_tx(self):
        """port_tx getter

        The name of a configured port

        Returns: str
        """
        return self._properties['port_tx']

    @port_tx.setter
    def port_tx(self, value):
        """port_tx setter

        The name of a configured port

        value: str
        """
        self._properties['port_tx'] = value

    @property
    def port_rx(self):
        """port_rx getter

        The name of a configured port

        Returns: str
        """
        return self._properties['port_rx']

    @port_rx.setter
    def port_rx(self, value):
        """port_rx setter

        The name of a configured port

        value: str
        """
        self._properties['port_rx'] = value

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

        The current total number of bytes received

        Returns: int
        """
        return self._properties['bytes_rx']

    @bytes_rx.setter
    def bytes_rx(self, value):
        """bytes_rx setter

        The current total number of bytes received

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
    def loss(self):
        """loss getter

        The percentage of lost frames

        Returns: float
        """
        return self._properties['loss']

    @loss.setter
    def loss(self, value):
        """loss setter

        The percentage of lost frames

        value: float
        """
        self._properties['loss'] = value

    @property
    def additionalProperties(self):
        """additionalProperties getter

        Any configured flow packet header field result_group names will appear as additional name/value pairs. result_group names will be the keys in string format. result_group values will be in number format.

        Returns: float
        """
        return self._properties['additionalProperties']

    @additionalProperties.setter
    def additionalProperties(self, value):
        """additionalProperties setter

        Any configured flow packet header field result_group names will appear as additional name/value pairs. result_group names will be the keys in string format. result_group values will be in number format.

        value: float
        """
        self._properties['additionalProperties'] = value
