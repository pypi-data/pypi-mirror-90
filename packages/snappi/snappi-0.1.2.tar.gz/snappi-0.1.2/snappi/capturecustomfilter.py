from .snappicommon import SnappiObject


class CaptureCustomFilter(SnappiObject):
    def __init__(self, filter=None, mask=None, offset=None):
        super(CaptureCustomFilter, self).__init__()
        self.filter = filter
        self.mask = mask
        self.offset = offset

    @property
    def filter(self):
        """filter getter

        The value to filter on.

        Returns: str
        """
        return self._properties['filter']

    @filter.setter
    def filter(self, value):
        """filter setter

        The value to filter on.

        value: str
        """
        self._properties['filter'] = value

    @property
    def mask(self):
        """mask getter

        The mask to be applied to the filter.

        Returns: str
        """
        return self._properties['mask']

    @mask.setter
    def mask(self, value):
        """mask setter

        The mask to be applied to the filter.

        value: str
        """
        self._properties['mask'] = value

    @property
    def offset(self):
        """offset getter

        The offset in the packet to filter at.

        Returns: int
        """
        return self._properties['offset']

    @offset.setter
    def offset(self, value):
        """offset setter

        The offset in the packet to filter at.

        value: int
        """
        self._properties['offset'] = value
