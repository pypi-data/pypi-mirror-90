from .snappicommon import SnappiObject


class CaptureRequest(SnappiObject):
    def __init__(self, port_name=None):
        super(CaptureRequest, self).__init__()
        self.port_name = port_name

    @property
    def port_name(self):
        """port_name getter

        The name of a port a capture is started on.

        Returns: str
        """
        return self._properties['port_name']

    @port_name.setter
    def port_name(self, value):
        """port_name setter

        The name of a port a capture is started on.

        value: str
        """
        self._properties['port_name'] = value
