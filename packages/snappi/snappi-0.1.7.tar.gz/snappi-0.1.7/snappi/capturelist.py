from .snappicommon import SnappiList


class CaptureList(SnappiList):
    def __init__(self):
        super(CaptureList, self).__init__()


    def capture(self, port_names=None, pcap=None, enable=True, overwrite=False, format='pcap', name=None):
        from .capture import Capture
        item = Capture(port_names, pcap, enable, overwrite, format, name)
        self._add(item)
        return self
