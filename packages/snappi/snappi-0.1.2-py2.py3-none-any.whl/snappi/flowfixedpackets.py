from .snappicommon import SnappiObject


class FlowFixedPackets(SnappiObject):
    def __init__(self, packets=None, gap=None, delay=None, delay_unit=None):
        super(FlowFixedPackets, self).__init__()
        self.packets = packets
        self.gap = gap
        self.delay = delay
        self.delay_unit = delay_unit

    @property
    def packets(self):
        """packets getter

        Stop transmit of the flow after this number of packets.

        Returns: int
        """
        return self._properties['packets']

    @packets.setter
    def packets(self, value):
        """packets setter

        Stop transmit of the flow after this number of packets.

        value: int
        """
        self._properties['packets'] = value

    @property
    def gap(self):
        """gap getter

        The minimum gap between packets expressed as bytes.

        Returns: int
        """
        return self._properties['gap']

    @gap.setter
    def gap(self, value):
        """gap setter

        The minimum gap between packets expressed as bytes.

        value: int
        """
        self._properties['gap'] = value

    @property
    def delay(self):
        """delay getter

        The delay before starting transmission of packets.

        Returns: int
        """
        return self._properties['delay']

    @delay.setter
    def delay(self, value):
        """delay setter

        The delay before starting transmission of packets.

        value: int
        """
        self._properties['delay'] = value

    @property
    def delay_unit(self):
        """delay_unit getter

        The delay expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._properties['delay_unit']

    @delay_unit.setter
    def delay_unit(self, value):
        """delay_unit setter

        The delay expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._properties['delay_unit'] = value
