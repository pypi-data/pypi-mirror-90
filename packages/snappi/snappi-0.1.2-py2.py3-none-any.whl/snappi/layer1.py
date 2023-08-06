from .snappicommon import SnappiObject


class Layer1(SnappiObject):
    _TYPES = {
        'auto_negotiation': '.layer1autonegotiation.Layer1AutoNegotiation',
        'flow_control': '.layer1flowcontrol.Layer1FlowControl',
    }

    def __init__(self, name=None, port_names=None, speed=None, media=None, promiscuous=None, mtu=None, ieee_media_defaults=None, auto_negotiate=None):
        super(Layer1, self).__init__()
        self.name = name
        self.port_names = port_names
        self.speed = speed
        self.media = media
        self.promiscuous = promiscuous
        self.mtu = mtu
        self.ieee_media_defaults = ieee_media_defaults
        self.auto_negotiate = auto_negotiate

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

        A list of unique names of port objects that will share the choice settings. 

        Returns: list[str]
        """
        return self._properties['port_names']

    @port_names.setter
    def port_names(self, value):
        """port_names setter

        A list of unique names of port objects that will share the choice settings. 

        value: list[str]
        """
        self._properties['port_names'] = value

    @property
    def speed(self):
        """speed getter

        Set the speed if supported.

        Returns: Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """
        return self._properties['speed']

    @speed.setter
    def speed(self, value):
        """speed setter

        Set the speed if supported.

        value: Union[speed_10_fd_mbps, speed_10_hd_mbps, speed_100_fd_mbps, speed_100_hd_mbps, speed_1_gbps, speed_10_gbps, speed_25_gbps, speed_40_gbps, speed_100_gbps, speed_200_gbps, speed_400_gbps]
        """
        self._properties['speed'] = value

    @property
    def media(self):
        """media getter

        Set the type of media interface if supported.

        Returns: Union[copper, fiber, sgmii]
        """
        return self._properties['media']

    @media.setter
    def media(self, value):
        """media setter

        Set the type of media interface if supported.

        value: Union[copper, fiber, sgmii]
        """
        self._properties['media'] = value

    @property
    def promiscuous(self):
        """promiscuous getter

        Enable promiscuous mode if supported.

        Returns: boolean
        """
        return self._properties['promiscuous']

    @promiscuous.setter
    def promiscuous(self, value):
        """promiscuous setter

        Enable promiscuous mode if supported.

        value: boolean
        """
        self._properties['promiscuous'] = value

    @property
    def mtu(self):
        """mtu getter

        Set the maximum transmission unit size if supported.

        Returns: int
        """
        return self._properties['mtu']

    @mtu.setter
    def mtu(self, value):
        """mtu setter

        Set the maximum transmission unit size if supported.

        value: int
        """
        self._properties['mtu'] = value

    @property
    def ieee_media_defaults(self):
        """ieee_media_defaults getter

        Set to true to override the auto_negotiate, link_training and rs_fec settings for gigabit ethernet interfaces.

        Returns: boolean
        """
        return self._properties['ieee_media_defaults']

    @ieee_media_defaults.setter
    def ieee_media_defaults(self, value):
        """ieee_media_defaults setter

        Set to true to override the auto_negotiate, link_training and rs_fec settings for gigabit ethernet interfaces.

        value: boolean
        """
        self._properties['ieee_media_defaults'] = value

    @property
    def auto_negotiate(self):
        """auto_negotiate getter

        Enable/disable auto negotiation.

        Returns: boolean
        """
        return self._properties['auto_negotiate']

    @auto_negotiate.setter
    def auto_negotiate(self, value):
        """auto_negotiate setter

        Enable/disable auto negotiation.

        value: boolean
        """
        self._properties['auto_negotiate'] = value

    @property
    def auto_negotiation(self):
        """auto_negotiation getter

        TBD

        Returns: obj(snappi.Layer1AutoNegotiation)
        """
        from .layer1autonegotiation import Layer1AutoNegotiation
        if 'auto_negotiation' not in self._properties or self._properties['auto_negotiation'] is None:
            self._properties['auto_negotiation'] = Layer1AutoNegotiation()
        return self._properties['auto_negotiation']

    @property
    def flow_control(self):
        """flow_control getter

        TBD

        Returns: obj(snappi.Layer1FlowControl)
        """
        from .layer1flowcontrol import Layer1FlowControl
        if 'flow_control' not in self._properties or self._properties['flow_control'] is None:
            self._properties['flow_control'] = Layer1FlowControl()
        return self._properties['flow_control']
