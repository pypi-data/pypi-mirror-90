from .snappicommon import SnappiObject


class FlowGre(SnappiObject):
    _TYPES = {
        'checksum_present': '.flowpattern.FlowPattern',
        'key_present': '.flowpattern.FlowPattern',
        'seq_number_present': '.flowpattern.FlowPattern',
        'reserved0': '.flowpattern.FlowPattern',
        'version': '.flowpattern.FlowPattern',
        'protocol': '.flowpattern.FlowPattern',
        'checksum': '.flowpattern.FlowPattern',
        'reserved1': '.flowpattern.FlowPattern',
        'key': '.flowpattern.FlowPattern',
        'sequence_number': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowGre, self).__init__()

    @property
    def checksum_present(self):
        """checksum_present getter

        A container for packet header field patterns.Checksum bit. Set to 1 if a checksum is present.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'checksum_present' not in self._properties or self._properties['checksum_present'] is None:
            self._properties['checksum_present'] = FlowPattern()
        return self._properties['checksum_present']

    @property
    def key_present(self):
        """key_present getter

        A container for packet header field patterns.Key bit. Set to 1 if a key is present.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'key_present' not in self._properties or self._properties['key_present'] is None:
            self._properties['key_present'] = FlowPattern()
        return self._properties['key_present']

    @property
    def seq_number_present(self):
        """seq_number_present getter

        A container for packet header field patterns.Sequence number bit. Set to 1 if a sequence number is present.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'seq_number_present' not in self._properties or self._properties['seq_number_present'] is None:
            self._properties['seq_number_present'] = FlowPattern()
        return self._properties['seq_number_present']

    @property
    def reserved0(self):
        """reserved0 getter

        A container for packet header field patterns.Reserved bits. Set to 0. 9 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'reserved0' not in self._properties or self._properties['reserved0'] is None:
            self._properties['reserved0'] = FlowPattern()
        return self._properties['reserved0']

    @property
    def version(self):
        """version getter

        A container for packet header field patterns.Gre version number. Set to 0. 3 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'version' not in self._properties or self._properties['version'] is None:
            self._properties['version'] = FlowPattern()
        return self._properties['version']

    @property
    def protocol(self):
        """protocol getter

        A container for packet header field patterns.Indicates the ether protocol type of the encapsulated payload. - 0x0800 ipv4 - 0x86DD ipv6

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'protocol' not in self._properties or self._properties['protocol'] is None:
            self._properties['protocol'] = FlowPattern()
        return self._properties['protocol']

    @property
    def checksum(self):
        """checksum getter

        A container for packet header field patterns.Present if the checksum_present bit is set. Contains the checksum for the gre header and payload. 16 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'checksum' not in self._properties or self._properties['checksum'] is None:
            self._properties['checksum'] = FlowPattern()
        return self._properties['checksum']

    @property
    def reserved1(self):
        """reserved1 getter

        A container for packet header field patterns.Reserved bits. Set to 0. 16 bits.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'reserved1' not in self._properties or self._properties['reserved1'] is None:
            self._properties['reserved1'] = FlowPattern()
        return self._properties['reserved1']

    @property
    def key(self):
        """key getter

        A container for packet header field patterns.Present if the key_present bit is set. Contains an application specific key value. 32 bits

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'key' not in self._properties or self._properties['key'] is None:
            self._properties['key'] = FlowPattern()
        return self._properties['key']

    @property
    def sequence_number(self):
        """sequence_number getter

        A container for packet header field patterns.Present if the seq_number_present bit is set. Contains a sequence number for the gre packet. 32 bits

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'sequence_number' not in self._properties or self._properties['sequence_number'] is None:
            self._properties['sequence_number'] = FlowPattern()
        return self._properties['sequence_number']
