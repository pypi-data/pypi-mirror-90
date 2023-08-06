from .snappicommon import SnappiObject


class Lag(SnappiObject):
    _TYPES = {
        'protocol': '.lagprotocol.LagProtocol',
        'ethernet': '.deviceethernet.DeviceEthernet',
    }

    def __init__(self, port_names=None, name=None):
        super(Lag, self).__init__()
        self.port_names = port_names
        self.name = name

    @property
    def port_names(self):
        """port_names getter

        A list of unique names of port objects that will be part of the same lag. The value of the port_names property is the count for any child property in this hierarchy that is a container for a device pattern.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        A list of unique names of port objects that will be part of the same lag. The value of the port_names property is the count for any child property in this hierarchy that is a container for a device pattern.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def protocol(self):
        """protocol getter

        Static lag or LACP protocol settings.

        Returns: obj(snappi.LagProtocol)
        """
        from .lagprotocol import LagProtocol
        if 'protocol' not in self._properties or self._properties['protocol'] is None:
            self._properties['protocol'] = LagProtocol()
        return self._properties['protocol']

    @property
    def ethernet(self):
        """ethernet getter

        Per port ethernet and vlan settings.

        Returns: obj(snappi.DeviceEthernet)
        """
        from .deviceethernet import DeviceEthernet
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = DeviceEthernet()
        return self._properties['ethernet']

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
