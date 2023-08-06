from .snappicommon import SnappiList


class FlowHeaderList(SnappiList):
    def __init__(self):
        super(FlowHeaderList, self).__init__()


    def flowheader(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        self._add(item)
        return self

    def custom(self, bytes=None):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.custom
        self._add(item)
        return self

    def ethernet(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.ethernet
        self._add(item)
        return self

    def vlan(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.vlan
        self._add(item)
        return self

    def vxlan(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.vxlan
        self._add(item)
        return self

    def ipv4(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.ipv4
        self._add(item)
        return self

    def ipv6(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.ipv6
        self._add(item)
        return self

    def pfcpause(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.pfcpause
        self._add(item)
        return self

    def ethernetpause(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.ethernetpause
        self._add(item)
        return self

    def tcp(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.tcp
        self._add(item)
        return self

    def udp(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.udp
        self._add(item)
        return self

    def gre(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.gre
        self._add(item)
        return self

    def gtpv1(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.gtpv1
        self._add(item)
        return self

    def gtpv2(self):
        from .flowheader import FlowHeader
        item = FlowHeader()
        item.gtpv2
        self._add(item)
        return self
