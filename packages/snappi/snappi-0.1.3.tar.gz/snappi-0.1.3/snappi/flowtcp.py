from .snappicommon import SnappiObject


class FlowTcp(SnappiObject):
    _TYPES = {
        'src_port': '.flowpattern.FlowPattern',
        'dst_port': '.flowpattern.FlowPattern',
        'seq_num': '.flowpattern.FlowPattern',
        'ack_num': '.flowpattern.FlowPattern',
        'data_offset': '.flowpattern.FlowPattern',
        'ecn_ns': '.flowpattern.FlowPattern',
        'ecn_cwr': '.flowpattern.FlowPattern',
        'ecn_echo': '.flowpattern.FlowPattern',
        'ctl_urg': '.flowpattern.FlowPattern',
        'ctl_ack': '.flowpattern.FlowPattern',
        'ctl_psh': '.flowpattern.FlowPattern',
        'ctl_rst': '.flowpattern.FlowPattern',
        'ctl_syn': '.flowpattern.FlowPattern',
        'ctl_fin': '.flowpattern.FlowPattern',
        'window': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowTcp, self).__init__()

    @property
    def src_port(self):
        """src_port getter

        A container for packet header field patterns.Tcp source port. Max length is 2 bytes.

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
    def seq_num(self):
        """seq_num getter

        A container for packet header field patterns.Tcp Sequence Number. Max length is 4 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'seq_num' not in self._properties or self._properties['seq_num'] is None:
            self._properties['seq_num'] = FlowPattern()
        return self._properties['seq_num']

    @property
    def ack_num(self):
        """ack_num getter

        A container for packet header field patterns.Tcp Acknowledgement Number. Max length is 4 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ack_num' not in self._properties or self._properties['ack_num'] is None:
            self._properties['ack_num'] = FlowPattern()
        return self._properties['ack_num']

    @property
    def data_offset(self):
        """data_offset getter

        A container for packet header field patterns.The number of 32 bit words in the TCP header. This indicates where the data begins. Max length is 4 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'data_offset' not in self._properties or self._properties['data_offset'] is None:
            self._properties['data_offset'] = FlowPattern()
        return self._properties['data_offset']

    @property
    def ecn_ns(self):
        """ecn_ns getter

        A container for packet header field patterns.Explicit congestion notification, concealment protection. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ecn_ns' not in self._properties or self._properties['ecn_ns'] is None:
            self._properties['ecn_ns'] = FlowPattern()
        return self._properties['ecn_ns']

    @property
    def ecn_cwr(self):
        """ecn_cwr getter

        A container for packet header field patterns.Explicit congestion notification, congestion window reduced. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ecn_cwr' not in self._properties or self._properties['ecn_cwr'] is None:
            self._properties['ecn_cwr'] = FlowPattern()
        return self._properties['ecn_cwr']

    @property
    def ecn_echo(self):
        """ecn_echo getter

        A container for packet header field patterns.Explicit congestion notification, echo. 1 indicates the peer is ecn capable. 0 indicates that a packet with ipv4.ecn = 11 in the ip header was received during normal transmission. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ecn_echo' not in self._properties or self._properties['ecn_echo'] is None:
            self._properties['ecn_echo'] = FlowPattern()
        return self._properties['ecn_echo']

    @property
    def ctl_urg(self):
        """ctl_urg getter

        A container for packet header field patterns.A value of 1 indicates that the urgent pointer field is significant. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ctl_urg' not in self._properties or self._properties['ctl_urg'] is None:
            self._properties['ctl_urg'] = FlowPattern()
        return self._properties['ctl_urg']

    @property
    def ctl_ack(self):
        """ctl_ack getter

        A container for packet header field patterns.A value of 1 indicates that the ackknowledgment field is significant. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ctl_ack' not in self._properties or self._properties['ctl_ack'] is None:
            self._properties['ctl_ack'] = FlowPattern()
        return self._properties['ctl_ack']

    @property
    def ctl_psh(self):
        """ctl_psh getter

        A container for packet header field patterns.Asks to push the buffered data to the receiving application. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ctl_psh' not in self._properties or self._properties['ctl_psh'] is None:
            self._properties['ctl_psh'] = FlowPattern()
        return self._properties['ctl_psh']

    @property
    def ctl_rst(self):
        """ctl_rst getter

        A container for packet header field patterns.Reset the connection. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ctl_rst' not in self._properties or self._properties['ctl_rst'] is None:
            self._properties['ctl_rst'] = FlowPattern()
        return self._properties['ctl_rst']

    @property
    def ctl_syn(self):
        """ctl_syn getter

        A container for packet header field patterns.Synchronize sequenece numbers. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ctl_syn' not in self._properties or self._properties['ctl_syn'] is None:
            self._properties['ctl_syn'] = FlowPattern()
        return self._properties['ctl_syn']

    @property
    def ctl_fin(self):
        """ctl_fin getter

        A container for packet header field patterns.Last packet from the sender. Max length is 1 bit.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ctl_fin' not in self._properties or self._properties['ctl_fin'] is None:
            self._properties['ctl_fin'] = FlowPattern()
        return self._properties['ctl_fin']

    @property
    def window(self):
        """window getter

        A container for packet header field patterns.Tcp connection window. Max length is 2 bytes.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'window' not in self._properties or self._properties['window'] is None:
            self._properties['window'] = FlowPattern()
        return self._properties['window']
