from .snappicommon import SnappiObject


class Capture(SnappiObject):
    _TYPES = {
        'basic': '.capturebasicfilterlist.CaptureBasicFilterList',
    }

    def __init__(self, name=None, port_names=None, enable=None, overwrite=None, format=None):
        super(Capture, self).__init__()
        self.name = name
        self.port_names = port_names
        self.enable = enable
        self.overwrite = overwrite
        self.format = format

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
    def port_names(self):
        """port_names getter

        The unique names of ports that the capture settings will apply to.

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        The unique names of ports that the capture settings will apply to.

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def choice(self):
        """choice getter

        The type of filter.

        Returns: Union[basic, pcap, choice, choice, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        The type of filter.

        value: Union[basic, pcap, choice, choice, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def basic(self):
        """basic getter

        An array of basic filters. The filters supported are source address, destination address and custom. 

        Returns: list[obj(snappi.CaptureBasicFilter)]
        """
        from .capturebasicfilterlist import CaptureBasicFilterList
        if 'basic' not in self._properties or self._properties['basic'] is None:
            self._properties['basic'] = CaptureBasicFilterList()
        return self._properties['basic']

    @property
    def pcap(self):
        """pcap getter

        The content of this property must be of pcap filter syntax. https://www.tcpdump.org/manpages/pcap-filter.7.html

        Returns: str
        """
        return self._properties['pcap']

    @pcap.setter
    def pcap(self, value):
        """pcap setter

        The content of this property must be of pcap filter syntax. https://www.tcpdump.org/manpages/pcap-filter.7.html

        value: str
        """
        self._properties['choice'] = 'pcap'
        self._properties['pcap'] = value

    @property
    def enable(self):
        """enable getter

        Enable capture on the port.

        Returns: boolean
        """
        return self._properties['enable']

    @enable.setter
    def enable(self, value):
        """enable setter

        Enable capture on the port.

        value: boolean
        """
        self._properties['enable'] = value

    @property
    def overwrite(self):
        """overwrite getter

        Overwrite the capture buffer.

        Returns: boolean
        """
        return self._properties['overwrite']

    @overwrite.setter
    def overwrite(self, value):
        """overwrite setter

        Overwrite the capture buffer.

        value: boolean
        """
        self._properties['overwrite'] = value

    @property
    def format(self):
        """format getter

        The format of the capture file.

        Returns: Union[pcap, pcapng]
        """
        return self._properties['format']

    @format.setter
    def format(self, value):
        """format setter

        The format of the capture file.

        value: Union[pcap, pcapng]
        """
        self._properties['format'] = value
