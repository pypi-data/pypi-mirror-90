from .snappicommon import SnappiObject


class FlowDuration(SnappiObject):
    _TYPES = {
        'fixed_packets': '.flowfixedpackets.FlowFixedPackets',
        'fixed_seconds': '.flowfixedseconds.FlowFixedSeconds',
        'burst': '.flowburst.FlowBurst',
        'continuous': '.flowcontinuous.FlowContinuous',
    }

    def __init__(self):
        super(FlowDuration, self).__init__()

    @property
    def fixed_packets(self):
        from .flowfixedpackets import FlowFixedPackets
        if 'fixed_packets' not in self._properties or self._properties['fixed_packets'] is None:
            self._properties['fixed_packets'] = FlowFixedPackets()
        self.choice = 'fixed_packets'
        return self._properties['fixed_packets']

    @property
    def fixed_seconds(self):
        from .flowfixedseconds import FlowFixedSeconds
        if 'fixed_seconds' not in self._properties or self._properties['fixed_seconds'] is None:
            self._properties['fixed_seconds'] = FlowFixedSeconds()
        self.choice = 'fixed_seconds'
        return self._properties['fixed_seconds']

    @property
    def burst(self):
        from .flowburst import FlowBurst
        if 'burst' not in self._properties or self._properties['burst'] is None:
            self._properties['burst'] = FlowBurst()
        self.choice = 'burst'
        return self._properties['burst']

    @property
    def continuous(self):
        from .flowcontinuous import FlowContinuous
        if 'continuous' not in self._properties or self._properties['continuous'] is None:
            self._properties['continuous'] = FlowContinuous()
        self.choice = 'continuous'
        return self._properties['continuous']

    @property
    def choice(self):
        """choice getter

        TBD

        Returns: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[fixed_packets, fixed_seconds, burst, continuous, choice, choice, choice]
        """
        self._properties['choice'] = value
