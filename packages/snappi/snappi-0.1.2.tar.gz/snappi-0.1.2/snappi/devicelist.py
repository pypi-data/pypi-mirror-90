from .snappicommon import SnappiList


class DeviceList(SnappiList):
    def __init__(self):
        super(DeviceList, self).__init__()


    def device(self, name=None, container_name=None, device_count=1):
        from .device import Device
        item = Device(name, container_name, device_count)
        self._add(item)
        return self

    def ethernet(self, name=None):
        from .device import Device
        item = Device()
        item.ethernet
        self._add(item)
        return self

    def ipv4(self, name=None):
        from .device import Device
        item = Device()
        item.ipv4
        self._add(item)
        return self

    def ipv6(self, name=None):
        from .device import Device
        item = Device()
        item.ipv6
        self._add(item)
        return self

    def bgpv4(self, name=None, as_type='None'):
        from .device import Device
        item = Device()
        item.bgpv4
        self._add(item)
        return self
