from .snappicommon import SnappiList


class Bgpv4MetricList(SnappiList):
    def __init__(self):
        super(Bgpv4MetricList, self).__init__()


    def bgpv4metric(self, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        from .bgpv4metric import Bgpv4Metric
        item = Bgpv4Metric(name, sessions_total, sessions_up, sessions_down, sessions_not_started, routes_advertised, routes_withdrawn)
        self._add(item)
        return self
