from .snappicommon import SnappiObject


class DeviceIpv4(SnappiObject):
    _TYPES = {
        'address': '.devicepattern.DevicePattern',
        'gateway': '.devicepattern.DevicePattern',
        'prefix': '.devicepattern.DevicePattern',
    }

    def __init__(self, name=None):
        super(DeviceIpv4, self).__init__()
        self.name = name

    @property
    def address(self):
        """address getter

        The ipv4 address.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'address' not in self._properties or self._properties['address'] is None:
            self._properties['address'] = DevicePattern()
        return self._properties['address']

    @property
    def gateway(self):
        """gateway getter

        The ipv4 address of the gateway.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'gateway' not in self._properties or self._properties['gateway'] is None:
            self._properties['gateway'] = DevicePattern()
        return self._properties['gateway']

    @property
    def prefix(self):
        """prefix getter

        The prefix of the ipv4 address.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'prefix' not in self._properties or self._properties['prefix'] is None:
            self._properties['prefix'] = DevicePattern()
        return self._properties['prefix']

    @property
    def name(self):
        """name getter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Globally unique name of an object. It also serves as the primary key for arrays of objects.

        value: str
        """
        self._properties['name'] = value
