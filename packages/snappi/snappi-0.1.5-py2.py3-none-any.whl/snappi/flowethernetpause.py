from .snappicommon import SnappiObject


class FlowEthernetPause(SnappiObject):
    _TYPES = {
        'dst': '.flowpattern.FlowPattern',
        'src': '.flowpattern.FlowPattern',
        'ether_type': '.flowpattern.FlowPattern',
        'control_op_code': '.flowpattern.FlowPattern',
        'time': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowEthernetPause, self).__init__()

    @property
    def dst(self):
        """dst getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'dst' not in self._properties or self._properties['dst'] is None:
            self._properties['dst'] = FlowPattern()
        return self._properties['dst']

    @property
    def src(self):
        """src getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'src' not in self._properties or self._properties['src'] is None:
            self._properties['src'] = FlowPattern()
        return self._properties['src']

    @property
    def ether_type(self):
        """ether_type getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ether_type' not in self._properties or self._properties['ether_type'] is None:
            self._properties['ether_type'] = FlowPattern()
        return self._properties['ether_type']

    @property
    def control_op_code(self):
        """control_op_code getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'control_op_code' not in self._properties or self._properties['control_op_code'] is None:
            self._properties['control_op_code'] = FlowPattern()
        return self._properties['control_op_code']

    @property
    def time(self):
        """time getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'time' not in self._properties or self._properties['time'] is None:
            self._properties['time'] = FlowPattern()
        return self._properties['time']
