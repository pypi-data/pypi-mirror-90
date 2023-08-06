from .snappicommon import SnappiObject


class FlowIpv4Tos(SnappiObject):
    _TYPES = {
        'precedence': '.flowpattern.FlowPattern',
        'delay': '.flowpattern.FlowPattern',
        'throughput': '.flowpattern.FlowPattern',
        'reliability': '.flowpattern.FlowPattern',
        'monetary': '.flowpattern.FlowPattern',
        'unused': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowIpv4Tos, self).__init__()

    @property
    def precedence(self):
        """precedence getter

        A container for packet header field patterns.Precedence value is 3 bits: >=0 precedence <=3

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'precedence' not in self._properties or self._properties['precedence'] is None:
            self._properties['precedence'] = FlowPattern()
        return self._properties['precedence']

    @property
    def delay(self):
        """delay getter

        A container for packet header field patterns.Delay value is 1 bit: >=0 delay <=1

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'delay' not in self._properties or self._properties['delay'] is None:
            self._properties['delay'] = FlowPattern()
        return self._properties['delay']

    @property
    def throughput(self):
        """throughput getter

        A container for packet header field patterns.Throughput value is 1 bit: >=0 throughput <=3

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'throughput' not in self._properties or self._properties['throughput'] is None:
            self._properties['throughput'] = FlowPattern()
        return self._properties['throughput']

    @property
    def reliability(self):
        """reliability getter

        A container for packet header field patterns.Reliability value is 1 bit: >=0 reliability <=1

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'reliability' not in self._properties or self._properties['reliability'] is None:
            self._properties['reliability'] = FlowPattern()
        return self._properties['reliability']

    @property
    def monetary(self):
        """monetary getter

        A container for packet header field patterns.Monetary value is 1 bit: >=0 monetary <=1

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'monetary' not in self._properties or self._properties['monetary'] is None:
            self._properties['monetary'] = FlowPattern()
        return self._properties['monetary']

    @property
    def unused(self):
        """unused getter

        A container for packet header field patterns.Unused value is 1 bit: >=0 unused <=1

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'unused' not in self._properties or self._properties['unused'] is None:
            self._properties['unused'] = FlowPattern()
        return self._properties['unused']
