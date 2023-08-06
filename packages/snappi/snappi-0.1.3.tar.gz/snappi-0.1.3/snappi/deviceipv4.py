from .snappicommon import SnappiObject


class DeviceIpv4(SnappiObject):
    _TYPES = {
        'address': '.devicepattern.DevicePattern',
        'gateway': '.devicepattern.DevicePattern',
        'prefix': '.devicepattern.DevicePattern',
        'ethernet': '.deviceethernet.DeviceEthernet',
    }

    def __init__(self, name=None):
        super(DeviceIpv4, self).__init__()
        self.name = name

    @property
    def name(self):
        """name getter

        Unique system wide name of an object that is also the primary key for objects found in arrays.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        Unique system wide name of an object that is also the primary key for objects found in arrays.

        value: str
        """
        self._properties['name'] = value

    @property
    def address(self):
        """address getter

        A container for emulated device property patterns.The ipv4 address.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'address' not in self._properties or self._properties['address'] is None:
            self._properties['address'] = DevicePattern()
        return self._properties['address']

    @property
    def gateway(self):
        """gateway getter

        A container for emulated device property patterns.The ipv4 address of the gateway.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'gateway' not in self._properties or self._properties['gateway'] is None:
            self._properties['gateway'] = DevicePattern()
        return self._properties['gateway']

    @property
    def prefix(self):
        """prefix getter

        A container for emulated device property patterns.The prefix of the ipv4 address.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'prefix' not in self._properties or self._properties['prefix'] is None:
            self._properties['prefix'] = DevicePattern()
        return self._properties['prefix']

    @property
    def ethernet(self):
        """ethernet getter

        Emulated ethernet protocol. A top level in the emulated device stack.

        Returns: obj(snappi.DeviceEthernet)
        """
        from .deviceethernet import DeviceEthernet
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = DeviceEthernet()
        return self._properties['ethernet']
