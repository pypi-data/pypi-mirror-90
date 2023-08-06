from .snappicommon import SnappiObject


class FlowIpv6(SnappiObject):
    _TYPES = {
        'version': '.flowpattern.FlowPattern',
        'traffic_class': '.flowpattern.FlowPattern',
        'flow_label': '.flowpattern.FlowPattern',
        'payload_length': '.flowpattern.FlowPattern',
        'next_header': '.flowpattern.FlowPattern',
        'hop_limit': '.flowpattern.FlowPattern',
        'src': '.flowpattern.FlowPattern',
        'dst': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowIpv6, self).__init__()

    @property
    def version(self):
        """version getter

        A container for packet header field patterns.Default version number is 6 (bit sequence 0110) 4 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'version' not in self._properties or self._properties['version'] is None:
            self._properties['version'] = FlowPattern()
        return self._properties['version']

    @property
    def traffic_class(self):
        """traffic_class getter

        A container for packet header field patterns.8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'traffic_class' not in self._properties or self._properties['traffic_class'] is None:
            self._properties['traffic_class'] = FlowPattern()
        return self._properties['traffic_class']

    @property
    def flow_label(self):
        """flow_label getter

        A container for packet header field patterns.20 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'flow_label' not in self._properties or self._properties['flow_label'] is None:
            self._properties['flow_label'] = FlowPattern()
        return self._properties['flow_label']

    @property
    def payload_length(self):
        """payload_length getter

        A container for packet header field patterns.16 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'payload_length' not in self._properties or self._properties['payload_length'] is None:
            self._properties['payload_length'] = FlowPattern()
        return self._properties['payload_length']

    @property
    def next_header(self):
        """next_header getter

        A container for packet header field patterns.8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'next_header' not in self._properties or self._properties['next_header'] is None:
            self._properties['next_header'] = FlowPattern()
        return self._properties['next_header']

    @property
    def hop_limit(self):
        """hop_limit getter

        A container for packet header field patterns.8 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'hop_limit' not in self._properties or self._properties['hop_limit'] is None:
            self._properties['hop_limit'] = FlowPattern()
        return self._properties['hop_limit']

    @property
    def src(self):
        """src getter

        A container for packet header field patterns.128 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'src' not in self._properties or self._properties['src'] is None:
            self._properties['src'] = FlowPattern()
        return self._properties['src']

    @property
    def dst(self):
        """dst getter

        A container for packet header field patterns.128 bits

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'dst' not in self._properties or self._properties['dst'] is None:
            self._properties['dst'] = FlowPattern()
        return self._properties['dst']
