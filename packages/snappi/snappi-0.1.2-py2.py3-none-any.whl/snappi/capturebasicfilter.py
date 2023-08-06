from .snappicommon import SnappiObject


class CaptureBasicFilter(SnappiObject):
    _TYPES = {
        'mac_address': '.capturemacaddressfilter.CaptureMacAddressFilter',
        'custom': '.capturecustomfilter.CaptureCustomFilter',
    }

    def __init__(self, and_operator=None, not_operator=None):
        super(CaptureBasicFilter, self).__init__()
        self.and_operator = and_operator
        self.not_operator = not_operator

    @property
    def mac_address(self):
        from .capturemacaddressfilter import CaptureMacAddressFilter
        if 'mac_address' not in self._properties or self._properties['mac_address'] is None:
            self._properties['mac_address'] = CaptureMacAddressFilter()
        self.choice = 'mac_address'
        return self._properties['mac_address']

    @property
    def custom(self):
        from .capturecustomfilter import CaptureCustomFilter
        if 'custom' not in self._properties or self._properties['custom'] is None:
            self._properties['custom'] = CaptureCustomFilter()
        self.choice = 'custom'
        return self._properties['custom']

    @property
    def choice(self):
        """choice getter

        TBD

        Returns: Union[mac_address, custom, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[mac_address, custom, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def and_operator(self):
        """and_operator getter

        TBD

        Returns: boolean
        """
        return self._properties['and_operator']

    @and_operator.setter
    def and_operator(self, value):
        """and_operator setter

        TBD

        value: boolean
        """
        self._properties['and_operator'] = value

    @property
    def not_operator(self):
        """not_operator getter

        TBD

        Returns: boolean
        """
        return self._properties['not_operator']

    @not_operator.setter
    def not_operator(self, value):
        """not_operator setter

        TBD

        value: boolean
        """
        self._properties['not_operator'] = value
