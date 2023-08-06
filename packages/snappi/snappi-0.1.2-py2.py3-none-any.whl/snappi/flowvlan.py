from .snappicommon import SnappiObject


class FlowVlan(SnappiObject):
    _TYPES = {
        'priority': '.flowpattern.FlowPattern',
        'cfi': '.flowpattern.FlowPattern',
        'id': '.flowpattern.FlowPattern',
        'protocol': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowVlan, self).__init__()

    @property
    def priority(self):
        """priority getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'priority' not in self._properties or self._properties['priority'] is None:
            self._properties['priority'] = FlowPattern()
        return self._properties['priority']

    @property
    def cfi(self):
        """cfi getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'cfi' not in self._properties or self._properties['cfi'] is None:
            self._properties['cfi'] = FlowPattern()
        return self._properties['cfi']

    @property
    def id(self):
        """id getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'id' not in self._properties or self._properties['id'] is None:
            self._properties['id'] = FlowPattern()
        return self._properties['id']

    @property
    def protocol(self):
        """protocol getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'protocol' not in self._properties or self._properties['protocol'] is None:
            self._properties['protocol'] = FlowPattern()
        return self._properties['protocol']
