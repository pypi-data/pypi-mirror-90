from .snappicommon import SnappiList


class PortMetricList(SnappiList):
    def __init__(self):
        super(PortMetricList, self).__init__()


    def metric(self, name=None, location=None, link='None', capture='None', frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, bytes_tx_rate=None, bytes_rx_rate=None):
        from .portmetric import PortMetric
        item = PortMetric(name, location, link, capture, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, bytes_tx_rate, bytes_rx_rate)
        self._add(item)
        return self
