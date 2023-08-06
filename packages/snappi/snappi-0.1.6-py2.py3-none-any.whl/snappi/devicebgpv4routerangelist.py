from .snappicommon import SnappiList


class DeviceBgpv4RouteRangeList(SnappiList):
    def __init__(self):
        super(DeviceBgpv4RouteRangeList, self).__init__()


    def bgpv4routerange(self, name=None, route_count_per_device=1):
        from .devicebgpv4routerange import DeviceBgpv4RouteRange
        item = DeviceBgpv4RouteRange(name, route_count_per_device)
        self._add(item)
        return self
