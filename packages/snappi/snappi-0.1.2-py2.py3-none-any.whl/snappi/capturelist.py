from .snappicommon import SnappiList


class CaptureList(SnappiList):
    def __init__(self):
        super(CaptureList, self).__init__()


    def capture(self, name=None, port_names=None, pcap=None, enable=True, overwrite=False, format='pcap'):
        from .capture import Capture
        item = Capture(name, port_names, pcap, enable, overwrite, format)
        self._add(item)
        return self
