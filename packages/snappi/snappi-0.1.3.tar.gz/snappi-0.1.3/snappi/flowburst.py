from .snappicommon import SnappiObject


class FlowBurst(SnappiObject):
    def __init__(self, packets=None, gap=None, inter_burst_gap=None, inter_burst_gap_unit=None):
        super(FlowBurst, self).__init__()
        self.packets = packets
        self.gap = gap
        self.inter_burst_gap = inter_burst_gap
        self.inter_burst_gap_unit = inter_burst_gap_unit

    @property
    def packets(self):
        """packets getter

        The number of packets transmitted per burst.

        Returns: int
        """
        return self._properties['packets']

    @packets.setter
    def packets(self, value):
        """packets setter

        The number of packets transmitted per burst.

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
    def inter_burst_gap(self):
        """inter_burst_gap getter

        The gap between the transmission of each burst. A value of 0 means there is no gap between bursts.

        Returns: int
        """
        return self._properties['inter_burst_gap']

    @inter_burst_gap.setter
    def inter_burst_gap(self, value):
        """inter_burst_gap setter

        The gap between the transmission of each burst. A value of 0 means there is no gap between bursts.

        value: int
        """
        self._properties['inter_burst_gap'] = value

    @property
    def inter_burst_gap_unit(self):
        """inter_burst_gap_unit getter

        The inter burst gap expressed as a number of this value.

        Returns: Union[bytes, nanoseconds]
        """
        return self._properties['inter_burst_gap_unit']

    @inter_burst_gap_unit.setter
    def inter_burst_gap_unit(self, value):
        """inter_burst_gap_unit setter

        The inter burst gap expressed as a number of this value.

        value: Union[bytes, nanoseconds]
        """
        self._properties['inter_burst_gap_unit'] = value
