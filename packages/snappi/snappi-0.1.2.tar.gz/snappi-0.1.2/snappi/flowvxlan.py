from .snappicommon import SnappiObject


class FlowVxlan(SnappiObject):
    _TYPES = {
        'flags': '.flowpattern.FlowPattern',
        'reserved0': '.flowpattern.FlowPattern',
        'vni': '.flowpattern.FlowPattern',
        'reserved1': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowVxlan, self).__init__()

    @property
    def flags(self):
        """flags getter

        A container for packet header field patterns.RRRRIRRR Where the I flag MUST be set to 1 for a valid vxlan network id (VNI). The other 7 bits (designated "R") are reserved fields and MUST be set to zero on transmission and ignored on receipt. 8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'flags' not in self._properties or self._properties['flags'] is None:
            self._properties['flags'] = FlowPattern()
        return self._properties['flags']

    @property
    def reserved0(self):
        """reserved0 getter

        A container for packet header field patterns.Set to 0. 24 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'reserved0' not in self._properties or self._properties['reserved0'] is None:
            self._properties['reserved0'] = FlowPattern()
        return self._properties['reserved0']

    @property
    def vni(self):
        """vni getter

        A container for packet header field patterns.Vxlan network id. 24 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'vni' not in self._properties or self._properties['vni'] is None:
            self._properties['vni'] = FlowPattern()
        return self._properties['vni']

    @property
    def reserved1(self):
        """reserved1 getter

        A container for packet header field patterns.Set to 0. 8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'reserved1' not in self._properties or self._properties['reserved1'] is None:
            self._properties['reserved1'] = FlowPattern()
        return self._properties['reserved1']
