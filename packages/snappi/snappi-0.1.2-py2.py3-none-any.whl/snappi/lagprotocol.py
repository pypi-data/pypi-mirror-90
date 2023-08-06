from .snappicommon import SnappiObject


class LagProtocol(SnappiObject):
    _TYPES = {
        'lacp': '.laglacp.LagLacp',
        'static': '.lagstatic.LagStatic',
    }

    def __init__(self):
        super(LagProtocol, self).__init__()

    @property
    def lacp(self):
        from .laglacp import LagLacp
        if 'lacp' not in self._properties or self._properties['lacp'] is None:
            self._properties['lacp'] = LagLacp()
        self.choice = 'lacp'
        return self._properties['lacp']

    @property
    def static(self):
        from .lagstatic import LagStatic
        if 'static' not in self._properties or self._properties['static'] is None:
            self._properties['static'] = LagStatic()
        self.choice = 'static'
        return self._properties['static']

    @property
    def choice(self):
        """choice getter

        The type of lag protocol.

        Returns: Union[lacp, static, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of lag protocol.

        value: Union[lacp, static, choice, choice, choice]
        """
        self._properties['choice'] = value
