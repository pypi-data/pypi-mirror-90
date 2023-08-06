from .snappicommon import SnappiObject


class FlowIpv4Dscp(SnappiObject):
    _TYPES = {
        'phb': '.flowpattern.FlowPattern',
        'ecn': '.flowpattern.FlowPattern',
    }

    PHB_DEFAULT = '0'
    PHB_CS1 = '8'
    PHB_CS2 = '16'
    PHB_CS3 = '24'
    PHB_CS4 = '32'
    PHB_CS5 = '40'
    PHB_CS6 = '48'
    PHB_CS7 = '56'
    PHB_AF11 = '10'
    PHB_AF12 = '12'
    PHB_AF13 = '14'
    PHB_AF21 = '18'
    PHB_AF22 = '20'
    PHB_AF23 = '22'
    PHB_AF31 = '26'
    PHB_AF32 = '28'
    PHB_AF33 = '30'
    PHB_AF41 = '34'
    PHB_AF42 = '36'
    PHB_AF43 = '38'
    PHB_EF46 = '46'
    ECN_NON_CAPABLE = '0'
    ECN_CAPABLE_TRANSPORT_0 = '1'
    ECN_CAPABLE_TRANSPORT_1 = '2'
    ECN_CONGESTION_ENCOUNTERED = '3'

    def __init__(self):
        super(FlowIpv4Dscp, self).__init__()

    @property
    def phb(self):
        """phb getter

        A container for packet header field patterns.phb (per-hop-behavior) value is 6 bits: >=0 PHB <=63.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'phb' not in self._properties or self._properties['phb'] is None:
            self._properties['phb'] = FlowPattern()
        return self._properties['phb']

    @property
    def ecn(self):
        """ecn getter

        A container for packet header field patterns.ecn (explicit-congestion-notification) value is 2 bits: >=0 ecn <=3

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ecn' not in self._properties or self._properties['ecn'] is None:
            self._properties['ecn'] = FlowPattern()
        return self._properties['ecn']
