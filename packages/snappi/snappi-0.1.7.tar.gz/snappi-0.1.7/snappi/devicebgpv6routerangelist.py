from .snappicommon import SnappiList


class DeviceBgpv6RouteRangeList(SnappiList):
    def __init__(self):
        super(DeviceBgpv6RouteRangeList, self).__init__()


    def bgpv6routerange(self, route_count_per_device=1, name=None):
        from .devicebgpv6routerange import DeviceBgpv6RouteRange
        item = DeviceBgpv6RouteRange(route_count_per_device, name)
        self._add(item)
        return self
