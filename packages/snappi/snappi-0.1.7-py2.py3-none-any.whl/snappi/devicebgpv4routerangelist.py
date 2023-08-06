from .snappicommon import SnappiList


class DeviceBgpv4RouteRangeList(SnappiList):
    def __init__(self):
        super(DeviceBgpv4RouteRangeList, self).__init__()


    def bgpv4routerange(self, route_count_per_device=1, name=None):
        from .devicebgpv4routerange import DeviceBgpv4RouteRange
        item = DeviceBgpv4RouteRange(route_count_per_device, name)
        self._add(item)
        return self
