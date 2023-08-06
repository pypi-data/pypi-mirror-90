from .snappicommon import SnappiObject


class FlowHeader(SnappiObject):
    _TYPES = {
        'custom': '.flowcustom.FlowCustom',
        'ethernet': '.flowethernet.FlowEthernet',
        'vlan': '.flowvlan.FlowVlan',
        'vxlan': '.flowvxlan.FlowVxlan',
        'ipv4': '.flowipv4.FlowIpv4',
        'ipv6': '.flowipv6.FlowIpv6',
        'pfcpause': '.flowpfcpause.FlowPfcPause',
        'ethernetpause': '.flowethernetpause.FlowEthernetPause',
        'tcp': '.flowtcp.FlowTcp',
        'udp': '.flowudp.FlowUdp',
        'gre': '.flowgre.FlowGre',
        'gtpv1': '.flowgtpv1.FlowGtpv1',
        'gtpv2': '.flowgtpv2.FlowGtpv2',
    }

    def __init__(self):
        super(FlowHeader, self).__init__()

    @property
    def custom(self):
        from .flowcustom import FlowCustom
        if 'custom' not in self._properties or self._properties['custom'] is None:
            self._properties['custom'] = FlowCustom()
        self.choice = 'custom'
        return self._properties['custom']

    @property
    def ethernet(self):
        from .flowethernet import FlowEthernet
        if 'ethernet' not in self._properties or self._properties['ethernet'] is None:
            self._properties['ethernet'] = FlowEthernet()
        self.choice = 'ethernet'
        return self._properties['ethernet']

    @property
    def vlan(self):
        from .flowvlan import FlowVlan
        if 'vlan' not in self._properties or self._properties['vlan'] is None:
            self._properties['vlan'] = FlowVlan()
        self.choice = 'vlan'
        return self._properties['vlan']

    @property
    def vxlan(self):
        from .flowvxlan import FlowVxlan
        if 'vxlan' not in self._properties or self._properties['vxlan'] is None:
            self._properties['vxlan'] = FlowVxlan()
        self.choice = 'vxlan'
        return self._properties['vxlan']

    @property
    def ipv4(self):
        from .flowipv4 import FlowIpv4
        if 'ipv4' not in self._properties or self._properties['ipv4'] is None:
            self._properties['ipv4'] = FlowIpv4()
        self.choice = 'ipv4'
        return self._properties['ipv4']

    @property
    def ipv6(self):
        from .flowipv6 import FlowIpv6
        if 'ipv6' not in self._properties or self._properties['ipv6'] is None:
            self._properties['ipv6'] = FlowIpv6()
        self.choice = 'ipv6'
        return self._properties['ipv6']

    @property
    def pfcpause(self):
        from .flowpfcpause import FlowPfcPause
        if 'pfcpause' not in self._properties or self._properties['pfcpause'] is None:
            self._properties['pfcpause'] = FlowPfcPause()
        self.choice = 'pfcpause'
        return self._properties['pfcpause']

    @property
    def ethernetpause(self):
        from .flowethernetpause import FlowEthernetPause
        if 'ethernetpause' not in self._properties or self._properties['ethernetpause'] is None:
            self._properties['ethernetpause'] = FlowEthernetPause()
        self.choice = 'ethernetpause'
        return self._properties['ethernetpause']

    @property
    def tcp(self):
        from .flowtcp import FlowTcp
        if 'tcp' not in self._properties or self._properties['tcp'] is None:
            self._properties['tcp'] = FlowTcp()
        self.choice = 'tcp'
        return self._properties['tcp']

    @property
    def udp(self):
        from .flowudp import FlowUdp
        if 'udp' not in self._properties or self._properties['udp'] is None:
            self._properties['udp'] = FlowUdp()
        self.choice = 'udp'
        return self._properties['udp']

    @property
    def gre(self):
        from .flowgre import FlowGre
        if 'gre' not in self._properties or self._properties['gre'] is None:
            self._properties['gre'] = FlowGre()
        self.choice = 'gre'
        return self._properties['gre']

    @property
    def gtpv1(self):
        from .flowgtpv1 import FlowGtpv1
        if 'gtpv1' not in self._properties or self._properties['gtpv1'] is None:
            self._properties['gtpv1'] = FlowGtpv1()
        self.choice = 'gtpv1'
        return self._properties['gtpv1']

    @property
    def gtpv2(self):
        from .flowgtpv2 import FlowGtpv2
        if 'gtpv2' not in self._properties or self._properties['gtpv2'] is None:
            self._properties['gtpv2'] = FlowGtpv2()
        self.choice = 'gtpv2'
        return self._properties['gtpv2']

    @property
    def choice(self):
        """choice getter

        TBD

        Returns: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[custom, ethernet, vlan, vxlan, ipv4, ipv6, pfcpause, ethernetpause, tcp, udp, gre, gtpv1, gtpv2, choice, choice, choice]
        """
        self._properties['choice'] = value
