from .snappicommon import SnappiObject


class FlowIpv4Priority(SnappiObject):
    _TYPES = {
        'raw': '.flowpattern.FlowPattern',
        'tos': '.flowipv4tos.FlowIpv4Tos',
        'dscp': '.flowipv4dscp.FlowIpv4Dscp',
    }

    def __init__(self):
        super(FlowIpv4Priority, self).__init__()

    @property
    def raw(self):
        from .flowpattern import FlowPattern
        if 'raw' not in self._properties or self._properties['raw'] is None:
            self._properties['raw'] = FlowPattern()
        self.choice = 'raw'
        return self._properties['raw']

    @property
    def tos(self):
        from .flowipv4tos import FlowIpv4Tos
        if 'tos' not in self._properties or self._properties['tos'] is None:
            self._properties['tos'] = FlowIpv4Tos()
        self.choice = 'tos'
        return self._properties['tos']

    @property
    def dscp(self):
        from .flowipv4dscp import FlowIpv4Dscp
        if 'dscp' not in self._properties or self._properties['dscp'] is None:
            self._properties['dscp'] = FlowIpv4Dscp()
        self.choice = 'dscp'
        return self._properties['dscp']

    @property
    def choice(self):
        """choice getter

        TBD

        Returns: Union[raw, tos, dscp, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[raw, tos, dscp, choice, choice, choice]
        """
        self._properties['choice'] = value
