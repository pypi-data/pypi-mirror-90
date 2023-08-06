from .snappicommon import SnappiObject


class DeviceBgpv6RouteRange(SnappiObject):
    _TYPES = {
        'address': '.devicepattern.DevicePattern',
        'prefix': '.devicepattern.DevicePattern',
        'as_path': '.devicepattern.DevicePattern',
        'next_hop_address': '.devicepattern.DevicePattern',
        'community': '.devicepattern.DevicePattern',
    }

    def __init__(self, name=None, route_count_per_device=None):
        super(DeviceBgpv6RouteRange, self).__init__()
        self.name = name
        self.route_count_per_device = route_count_per_device

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
    def route_count_per_device(self):
        """route_count_per_device getter

        The number of routes per device.

        Returns: int
        """
        return self._properties['route_count_per_device']

    @route_count_per_device.setter
    def route_count_per_device(self, value):
        """route_count_per_device setter

        The number of routes per device.

        value: int
        """
        self._properties['route_count_per_device'] = value

    @property
    def address(self):
        """address getter

        The network address of the first network

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'address' not in self._properties or self._properties['address'] is None:
            self._properties['address'] = DevicePattern()
        return self._properties['address']

    @property
    def prefix(self):
        """prefix getter

        Ipv6 prefix length with minimum value is 0 to maximum value is 128

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'prefix' not in self._properties or self._properties['prefix'] is None:
            self._properties['prefix'] = DevicePattern()
        return self._properties['prefix']

    @property
    def as_path(self):
        """as_path getter

        Autonomous Systems (AS) numbers that a route passes through to reach the destination

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'as_path' not in self._properties or self._properties['as_path'] is None:
            self._properties['as_path'] = DevicePattern()
        return self._properties['as_path']

    @property
    def next_hop_address(self):
        """next_hop_address getter

        IP Address of next router to forward a packet to its final destination

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'next_hop_address' not in self._properties or self._properties['next_hop_address'] is None:
            self._properties['next_hop_address'] = DevicePattern()
        return self._properties['next_hop_address']

    @property
    def community(self):
        """community getter

        BGP communities provide additional capability for tagging routes and for modifying BGP routing policy on upstream and downstream routers BGP community is a 32-bit number which broken into 16-bit As and 16-bit custom value Please specify those two values in this string format 65000:100

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'community' not in self._properties or self._properties['community'] is None:
            self._properties['community'] = DevicePattern()
        return self._properties['community']
