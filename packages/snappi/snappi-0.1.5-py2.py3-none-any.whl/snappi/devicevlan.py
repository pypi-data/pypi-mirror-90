from .snappicommon import SnappiObject


class DeviceVlan(SnappiObject):
    _TYPES = {
        'tpid': '.devicepattern.DevicePattern',
        'priority': '.devicepattern.DevicePattern',
        'id': '.devicepattern.DevicePattern',
    }

    def __init__(self, name=None):
        super(DeviceVlan, self).__init__()
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
    def tpid(self):
        """tpid getter

        Vlan tag protocol identifier.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'tpid' not in self._properties or self._properties['tpid'] is None:
            self._properties['tpid'] = DevicePattern()
        return self._properties['tpid']

    @property
    def priority(self):
        """priority getter

        Vlan priority.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'priority' not in self._properties or self._properties['priority'] is None:
            self._properties['priority'] = DevicePattern()
        return self._properties['priority']

    @property
    def id(self):
        """id getter

        Vlan id.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'id' not in self._properties or self._properties['id'] is None:
            self._properties['id'] = DevicePattern()
        return self._properties['id']
