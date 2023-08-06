from .snappicommon import SnappiObject


class FlowGtpv1(SnappiObject):
    _TYPES = {
        'version': '.flowpattern.FlowPattern',
        'protocol_type': '.flowpattern.FlowPattern',
        'reserved': '.flowpattern.FlowPattern',
        'e_flag': '.flowpattern.FlowPattern',
        's_flag': '.flowpattern.FlowPattern',
        'pn_flag': '.flowpattern.FlowPattern',
        'message_type': '.flowpattern.FlowPattern',
        'message_length': '.flowpattern.FlowPattern',
        'teid': '.flowpattern.FlowPattern',
        'squence_number': '.flowpattern.FlowPattern',
        'n_pdu_number': '.flowpattern.FlowPattern',
        'next_extension_header_type': '.flowpattern.FlowPattern',
        'extension_headers': '.flowgtpextensionlist.FlowGtpExtensionList',
    }

    def __init__(self):
        super(FlowGtpv1, self).__init__()

    @property
    def version(self):
        """version getter

        A container for packet header field patterns.It is a 3-bit field. For GTPv1, this has a value of 1.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'version' not in self._properties or self._properties['version'] is None:
            self._properties['version'] = FlowPattern()
        return self._properties['version']

    @property
    def protocol_type(self):
        """protocol_type getter

        A container for packet header field patterns.A 1-bit value that differentiates GTP (value 1) from GTP' (value 0).

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'protocol_type' not in self._properties or self._properties['protocol_type'] is None:
            self._properties['protocol_type'] = FlowPattern()
        return self._properties['protocol_type']

    @property
    def reserved(self):
        """reserved getter

        A container for packet header field patterns.A 1-bit reserved field (must be 0).

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'reserved' not in self._properties or self._properties['reserved'] is None:
            self._properties['reserved'] = FlowPattern()
        return self._properties['reserved']

    @property
    def e_flag(self):
        """e_flag getter

        A container for packet header field patterns.A 1-bit value that states whether there is an extension header optional field.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'e_flag' not in self._properties or self._properties['e_flag'] is None:
            self._properties['e_flag'] = FlowPattern()
        return self._properties['e_flag']

    @property
    def s_flag(self):
        """s_flag getter

        A container for packet header field patterns.A 1-bit value that states whether there is a Sequence Number optional field.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 's_flag' not in self._properties or self._properties['s_flag'] is None:
            self._properties['s_flag'] = FlowPattern()
        return self._properties['s_flag']

    @property
    def pn_flag(self):
        """pn_flag getter

        A container for packet header field patterns.A 1-bit value that states whether there is a N-PDU number optional field.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'pn_flag' not in self._properties or self._properties['pn_flag'] is None:
            self._properties['pn_flag'] = FlowPattern()
        return self._properties['pn_flag']

    @property
    def message_type(self):
        """message_type getter

        A container for packet header field patterns.An 8-bit field that indicates the type of GTP message. Different types of messages are defined in 3GPP TS 29.060 section 7.1

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'message_type' not in self._properties or self._properties['message_type'] is None:
            self._properties['message_type'] = FlowPattern()
        return self._properties['message_type']

    @property
    def message_length(self):
        """message_length getter

        A container for packet header field patterns.A 16-bit field that indicates the length of the payload in bytes (rest of the packet following the mandatory 8-byte GTP header). Includes the optional fields.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'message_length' not in self._properties or self._properties['message_length'] is None:
            self._properties['message_length'] = FlowPattern()
        return self._properties['message_length']

    @property
    def teid(self):
        """teid getter

        A container for packet header field patterns.Tunnel endpoint identifier. A 32-bit(4-octet) field used to multiplex different connections in the same GTP tunnel.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'teid' not in self._properties or self._properties['teid'] is None:
            self._properties['teid'] = FlowPattern()
        return self._properties['teid']

    @property
    def squence_number(self):
        """squence_number getter

        A container for packet header field patterns.An (optional) 16-bit field. This field exists if any of the e_flag, s_flag, or pn_flag bits are on. The field must be interpreted only if the s_flag bit is on.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'squence_number' not in self._properties or self._properties['squence_number'] is None:
            self._properties['squence_number'] = FlowPattern()
        return self._properties['squence_number']

    @property
    def n_pdu_number(self):
        """n_pdu_number getter

        A container for packet header field patterns.An (optional) 8-bit field. This field exists if any of the e_flag, s_flag, or pn_flag bits are on. The field must be interpreted only if the pn_flag bit is on.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'n_pdu_number' not in self._properties or self._properties['n_pdu_number'] is None:
            self._properties['n_pdu_number'] = FlowPattern()
        return self._properties['n_pdu_number']

    @property
    def next_extension_header_type(self):
        """next_extension_header_type getter

        A container for packet header field patterns.An (optional) 8-bit field. This field exists if any of the e_flag, s_flag, or pn_flag bits are on. The field must be interpreted only if the e_flag bit is on.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'next_extension_header_type' not in self._properties or self._properties['next_extension_header_type'] is None:
            self._properties['next_extension_header_type'] = FlowPattern()
        return self._properties['next_extension_header_type']

    @property
    def extension_headers(self):
        """extension_headers getter

        A list of optional extension headers.

        Returns: list[obj(snappi.FlowGtpExtension)]
        """
        from .flowgtpextensionlist import FlowGtpExtensionList
        if 'extension_headers' not in self._properties or self._properties['extension_headers'] is None:
            self._properties['extension_headers'] = FlowGtpExtensionList()
        return self._properties['extension_headers']
