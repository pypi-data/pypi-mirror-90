from .snappicommon import SnappiList


class DeviceVlanList(SnappiList):
    def __init__(self):
        super(DeviceVlanList, self).__init__()


    def vlan(self, name=None):
        from .devicevlan import DeviceVlan
        item = DeviceVlan(name)
        self._add(item)
        return self
