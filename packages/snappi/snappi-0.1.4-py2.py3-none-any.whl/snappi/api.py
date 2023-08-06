from .snappicommon import SnappiRestTransport


class Api(SnappiRestTransport):
    """Snappi Abstract API
    """
    def __init__(self):
        super(Api, self).__init__()

    def set_config(self, content):
        """POST /config

        Sets configuration resources on the traffic generator.
        """
        return self.send_recv('post', '/config', payload=content)

    def update_config(self, content):
        """PATCH /config

        Updates configuration resources on the traffic generator.
        """
        return self.send_recv('patch', '/config', payload=content)

    def get_config(self):
        """GET /config

        TBD
        """
        return self.send_recv('get', '/config', return_object=self.config())

    def set_transmit_state(self, content):
        """POST /control/transmit

        Updates the state of configuration resources on the traffic generator.
        """
        return self.send_recv('post', '/control/transmit', payload=content)

    def set_link_state(self, content):
        """POST /control/link

        Updates the state of configuration resources on the traffic generator.
        """
        return self.send_recv('post', '/control/link', payload=content)

    def set_capture_state(self, content):
        """POST /control/capture

        Updates the state of configuration resources on the traffic generator.
        """
        return self.send_recv('post', '/control/capture', payload=content)

    def get_state_metrics(self):
        """POST /results/state

        TBD
        """
        return self.send_recv('post', '/results/state', return_object=self.state_metrics())

    def get_capabilities(self):
        """POST /results/capabilities

        TBD
        """
        return self.send_recv('post', '/results/capabilities', return_object=self.capabilities())

    def get_port_metrics(self, content):
        """POST /results/port

        TBD
        """
        return self.send_recv('post', '/results/port', payload=content, return_object=self.port_metrics())

    def get_capture(self, content):
        """POST /results/capture

        TBD
        """
        return self.send_recv('post', '/results/capture', payload=content)

    def get_flow_metrics(self, content):
        """POST /results/flow

        TBD
        """
        return self.send_recv('post', '/results/flow', payload=content, return_object=self.flow_metrics())

    def get_bgpv4_metrics(self, content):
        """POST /results/bgpv4

        TBD
        """
        return self.send_recv('post', '/results/bgpv4', payload=content, return_object=self.bgpv4_metrics())

    def config(self):
        """Return instance of auto-generated top level class Config
        """
        from .config import Config
        return Config()

    def transmit_state(self):
        """Return instance of auto-generated top level class TransmitState
        """
        from .transmitstate import TransmitState
        return TransmitState()

    def link_state(self):
        """Return instance of auto-generated top level class LinkState
        """
        from .linkstate import LinkState
        return LinkState()

    def capture_state(self):
        """Return instance of auto-generated top level class CaptureState
        """
        from .capturestate import CaptureState
        return CaptureState()

    def state_metrics(self):
        """Return instance of auto-generated top level class StateMetrics
        """
        from .statemetrics import StateMetrics
        return StateMetrics()

    def capabilities(self):
        """Return instance of auto-generated top level class Capabilities
        """
        from .capabilities import Capabilities
        return Capabilities()

    def port_metrics_request(self):
        """Return instance of auto-generated top level class PortMetricsRequest
        """
        from .portmetricsrequest import PortMetricsRequest
        return PortMetricsRequest()

    def port_metrics(self):
        """Return instance of auto-generated top level class PortMetricList
        """
        from .portmetriclist import PortMetricList
        return PortMetricList()

    def capture_request(self):
        """Return instance of auto-generated top level class CaptureRequest
        """
        from .capturerequest import CaptureRequest
        return CaptureRequest()

    def flow_metrics_request(self):
        """Return instance of auto-generated top level class FlowMetricsRequest
        """
        from .flowmetricsrequest import FlowMetricsRequest
        return FlowMetricsRequest()

    def flow_metrics(self):
        """Return instance of auto-generated top level class FlowMetricList
        """
        from .flowmetriclist import FlowMetricList
        return FlowMetricList()

    def bgpv4_metrics_request(self):
        """Return instance of auto-generated top level class Bgpv4MetricsRequest
        """
        from .bgpv4metricsrequest import Bgpv4MetricsRequest
        return Bgpv4MetricsRequest()

    def bgpv4_metrics(self):
        """Return instance of auto-generated top level class Bgpv4Metrics
        """
        from .bgpv4metrics import Bgpv4Metrics
        return Bgpv4Metrics()
