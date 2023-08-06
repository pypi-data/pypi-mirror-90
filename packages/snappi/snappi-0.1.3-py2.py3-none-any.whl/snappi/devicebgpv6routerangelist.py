from .snappicommon import SnappiList


class DeviceBgpv6RouteRangeList(SnappiList):
    def __init__(self):
        super(DeviceBgpv6RouteRangeList, self).__init__()


    def devicebgpv6routerange(self, name=None, route_count_per_device=1):
        from .devicebgpv6routerange import DeviceBgpv6RouteRange
        item = DeviceBgpv6RouteRange(name, route_count_per_device)
        self._add(item)
        return self
