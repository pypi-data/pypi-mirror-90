from .snappicommon import SnappiList


class FlowMetricList(SnappiList):
    def __init__(self):
        super(FlowMetricList, self).__init__()


    def flowmetric(self, name=None, transmit='None', port_tx=None, port_rx=None, frames_tx=None, frames_rx=None, bytes_tx=None, bytes_rx=None, frames_tx_rate=None, frames_rx_rate=None, loss=None, additionalProperties=None):
        from .flowmetric import FlowMetric
        item = FlowMetric(name, transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss, additionalProperties)
        self._add(item)
        return self
