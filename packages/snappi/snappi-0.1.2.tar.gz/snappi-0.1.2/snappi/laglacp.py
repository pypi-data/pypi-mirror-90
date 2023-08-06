from .snappicommon import SnappiObject


class LagLacp(SnappiObject):
    _TYPES = {
        'actor_key': '.devicepattern.DevicePattern',
        'actor_port_number': '.devicepattern.DevicePattern',
        'actor_port_priority': '.devicepattern.DevicePattern',
        'actor_system_id': '.devicepattern.DevicePattern',
        'actor_system_priority': '.devicepattern.DevicePattern',
    }

    def __init__(self):
        super(LagLacp, self).__init__()

    @property
    def actor_key(self):
        """actor_key getter

        A container for emulated device property patterns.The actor key.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'actor_key' not in self._properties or self._properties['actor_key'] is None:
            self._properties['actor_key'] = DevicePattern()
        return self._properties['actor_key']

    @property
    def actor_port_number(self):
        """actor_port_number getter

        A container for emulated device property patterns.The actor port number.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'actor_port_number' not in self._properties or self._properties['actor_port_number'] is None:
            self._properties['actor_port_number'] = DevicePattern()
        return self._properties['actor_port_number']

    @property
    def actor_port_priority(self):
        """actor_port_priority getter

        A container for emulated device property patterns.The actor port priority.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'actor_port_priority' not in self._properties or self._properties['actor_port_priority'] is None:
            self._properties['actor_port_priority'] = DevicePattern()
        return self._properties['actor_port_priority']

    @property
    def actor_system_id(self):
        """actor_system_id getter

        A container for emulated device property patterns.The actor system id.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'actor_system_id' not in self._properties or self._properties['actor_system_id'] is None:
            self._properties['actor_system_id'] = DevicePattern()
        return self._properties['actor_system_id']

    @property
    def actor_system_priority(self):
        """actor_system_priority getter

        A container for emulated device property patterns.The actor system priority.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'actor_system_priority' not in self._properties or self._properties['actor_system_priority'] is None:
            self._properties['actor_system_priority'] = DevicePattern()
        return self._properties['actor_system_priority']
