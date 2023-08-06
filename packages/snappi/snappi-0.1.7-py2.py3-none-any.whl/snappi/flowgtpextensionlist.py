from .snappicommon import SnappiList


class FlowGtpExtensionList(SnappiList):
    def __init__(self):
        super(FlowGtpExtensionList, self).__init__()


    def gtpextension(self):
        from .flowgtpextension import FlowGtpExtension
        item = FlowGtpExtension()
        self._add(item)
        return self
