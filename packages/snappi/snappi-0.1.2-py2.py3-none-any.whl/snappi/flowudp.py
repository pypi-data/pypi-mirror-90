from .snappicommon import SnappiObject


class FlowUdp(SnappiObject):
    _TYPES = {
        'src_port': '.flowpattern.FlowPattern',
        'dst_port': '.flowpattern.FlowPattern',
        'length': '.flowpattern.FlowPattern',
        'checksum': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowUdp, self).__init__()

    @property
    def src_port(self):
        """src_port getter

        A container for packet header field patterns.Udp source port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'src_port' not in self._properties or self._properties['src_port'] is None:
            self._properties['src_port'] = FlowPattern()
        return self._properties['src_port']

    @property
    def dst_port(self):
        """dst_port getter

        A container for packet header field patterns.Tcp destination port. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'dst_port' not in self._properties or self._properties['dst_port'] is None:
            self._properties['dst_port'] = FlowPattern()
        return self._properties['dst_port']

    @property
    def length(self):
        """length getter

        A container for packet header field patterns.Length in bytes of the udp header and yudp data. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'length' not in self._properties or self._properties['length'] is None:
            self._properties['length'] = FlowPattern()
        return self._properties['length']

    @property
    def checksum(self):
        """checksum getter

        A container for packet header field patterns.Checksum field used for error checking of header and data. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'checksum' not in self._properties or self._properties['checksum'] is None:
            self._properties['checksum'] = FlowPattern()
        return self._properties['checksum']
