from .snappicommon import SnappiObject


class Device(SnappiObject):
    _TYPES = {
        'ethernet': '.deviceethernet.DeviceEthernet',
        'ipv4': '.deviceipv4.DeviceIpv4',
        'ipv6': '.deviceipv6.DeviceIpv6',
        'bgpv4': '.devicebgpv4.DeviceBgpv4',
    }

    def __init__(self, name=None, container_name=None, device_count=None):
        super(Device, self).__init__()
        self.name = name
        self.container_name = container_name
        self.device_count = device_count

    @property
    def ethernet(self):
        from .deviceethernet import DeviceEthernet
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = DeviceEthernet()
        self.choice = 'ethernet'
        return self._properties['ethernet']

    @property
    def ipv4(self):
        from .deviceipv4 import DeviceIpv4
        if 'ipv4' not in self._properties or self._properties['ipv4'] is None:
            self._properties['ipv4'] = DeviceIpv4()
        self.choice = 'ipv4'
        return self._properties['ipv4']

    @property
    def ipv6(self):
        from .deviceipv6 import DeviceIpv6
        if 'ipv6' not in self._properties or self._properties['ipv6'] is None:
            self._properties['ipv6'] = DeviceIpv6()
        self.choice = 'ipv6'
        return self._properties['ipv6']

    @property
    def bgpv4(self):
        from .devicebgpv4 import DeviceBgpv4
        if 'bgpv4' not in self._properties or self._properties['bgpv4'] is None:
            self._properties['bgpv4'] = DeviceBgpv4()
        self.choice = 'bgpv4'
        return self._properties['bgpv4']

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
    def container_name(self):
        """container_name getter

        The unique name of a Port or Lag object that will contain the emulated interfaces and/or devices.

        Returns: str
        """
        return self._properties['container_name']

    @container_name.setter
    def container_name(self, value):
        """container_name setter

        The unique name of a Port or Lag object that will contain the emulated interfaces and/or devices.

        value: str
        """
        self._properties['container_name'] = value

    @property
    def device_count(self):
        """device_count getter

        The number of emulated protocol devices or interfaces per port.. Example: If the device_count is 10 and the choice property value is ethernet then an implementation MUST create 10 ethernet interfaces. The ethernet property is a container for src, dst and eth_type properties with each on of those properties being a pattern container for 10 possible values. . If an implementation is unable to support the maximum device_count it MUST indicate what the maximum device_count is using the /results/capabilities API.. The device_count is also used by the individual child properties that are a container for a /components/schemas/Device.Pattern.

        Returns: int
        """
        return self._properties['device_count']

    @device_count.setter
    def device_count(self, value):
        """device_count setter

        The number of emulated protocol devices or interfaces per port.. Example: If the device_count is 10 and the choice property value is ethernet then an implementation MUST create 10 ethernet interfaces. The ethernet property is a container for src, dst and eth_type properties with each on of those properties being a pattern container for 10 possible values. . If an implementation is unable to support the maximum device_count it MUST indicate what the maximum device_count is using the /results/capabilities API.. The device_count is also used by the individual child properties that are a container for a /components/schemas/Device.Pattern.

        value: int
        """
        self._properties['device_count'] = value

    @property
    def choice(self):
        """choice getter

        The type of emulated protocol interface or device.

        Returns: Union[ethernet, ipv4, ipv6, bgpv4, choice, choice, choice, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of emulated protocol interface or device.

        value: Union[ethernet, ipv4, ipv6, bgpv4, choice, choice, choice, choice, choice, choice]
        """
        self._properties['choice'] = value
