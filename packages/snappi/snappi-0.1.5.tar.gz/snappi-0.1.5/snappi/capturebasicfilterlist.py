from .snappicommon import SnappiList


class CaptureBasicFilterList(SnappiList):
    def __init__(self):
        super(CaptureBasicFilterList, self).__init__()


    def basicfilter(self, and_operator=True, not_operator=False):
        from .capturebasicfilter import CaptureBasicFilter
        item = CaptureBasicFilter(and_operator, not_operator)
        self._add(item)
        return self

    def mac_address(self, mac='None', filter=None, mask=None):
        from .capturebasicfilter import CaptureBasicFilter
        item = CaptureBasicFilter()
        item.mac_address
        self._add(item)
        return self

    def custom(self, filter=None, mask=None, offset=None):
        from .capturebasicfilter import CaptureBasicFilter
        item = CaptureBasicFilter()
        item.custom
        self._add(item)
        return self
