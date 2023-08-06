from .snappicommon import SnappiObject


class FlowFixedSeconds(SnappiObject):
    def __init__(self, seconds=None, gap=None, delay=None, delay_unit=None):
        super(FlowFixedSeconds, self).__init__()
        self.seconds = seconds
        self.gap = gap
        self.delay = delay
        self.delay_unit = delay_unit

    @property
    def seconds(self):
        """seconds getter

        Stop transmit of the flow after this number of seconds.

        Returns: float
        """
        return self._properties['seconds']

    @seconds.setter
    def seconds(self, value):
        """seconds setter

        Stop transmit of the flow after this number of seconds.

        value: float
        """
        self._properties['seconds'] = value

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
