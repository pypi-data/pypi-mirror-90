from .snappicommon import SnappiObject


class FlowRate(SnappiObject):
    def __init__(self):
        super(FlowRate, self).__init__()

    @property
    def choice(self):
        """choice getter

        TBD

        Returns: Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[pps, bps, kbps, mbps, gbps, percentage, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def pps(self):
        """pps getter

        Packets per second.

        Returns: int
        """
        return self._properties['pps']

    @pps.setter
    def pps(self, value):
        """pps setter

        Packets per second.

        value: int
        """
        self._properties['choice'] = 'pps'
        self._properties['pps'] = value

    @property
    def bps(self):
        """bps getter

        Bits per second.

        Returns: int
        """
        return self._properties['bps']

    @bps.setter
    def bps(self, value):
        """bps setter

        Bits per second.

        value: int
        """
        self._properties['choice'] = 'bps'
        self._properties['bps'] = value

    @property
    def kbps(self):
        """kbps getter

        Kilobits per second.

        Returns: int
        """
        return self._properties['kbps']

    @kbps.setter
    def kbps(self, value):
        """kbps setter

        Kilobits per second.

        value: int
        """
        self._properties['choice'] = 'kbps'
        self._properties['kbps'] = value

    @property
    def mbps(self):
        """mbps getter

        Megabits per second.

        Returns: int
        """
        return self._properties['mbps']

    @mbps.setter
    def mbps(self, value):
        """mbps setter

        Megabits per second.

        value: int
        """
        self._properties['choice'] = 'mbps'
        self._properties['mbps'] = value

    @property
    def gbps(self):
        """gbps getter

        Gigabits per second.

        Returns: int
        """
        return self._properties['gbps']

    @gbps.setter
    def gbps(self, value):
        """gbps setter

        Gigabits per second.

        value: int
        """
        self._properties['choice'] = 'gbps'
        self._properties['gbps'] = value

    @property
    def percentage(self):
        """percentage getter

        The percentage of a port location's available bandwidth.

        Returns: float
        """
        return self._properties['percentage']

    @percentage.setter
    def percentage(self, value):
        """percentage setter

        The percentage of a port location's available bandwidth.

        value: float
        """
        self._properties['choice'] = 'percentage'
        self._properties['percentage'] = value
