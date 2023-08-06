from .snappicommon import SnappiObject


class FlowBitList(SnappiObject):
    def __init__(self, offset=None, length=None, count=None, values=None):
        super(FlowBitList, self).__init__()
        self.offset = offset
        self.length = length
        self.count = count
        self.values = values

    @property
    def offset(self):
        """offset getter

        Bit offset in the packet at which the pattern will be applied

        Returns: int
        """
        return self._properties['offset']

    @offset.setter
    def offset(self, value):
        """offset setter

        Bit offset in the packet at which the pattern will be applied

        value: int
        """
        self._properties['offset'] = value

    @property
    def length(self):
        """length getter

        The number of bits in the packet that the pattern will span

        Returns: int
        """
        return self._properties['length']

    @length.setter
    def length(self, value):
        """length setter

        The number of bits in the packet that the pattern will span

        value: int
        """
        self._properties['length'] = value

    @property
    def count(self):
        """count getter

        The number of values to generate before repeating

        Returns: int
        """
        return self._properties['count']

    @count.setter
    def count(self, value):
        """count setter

        The number of values to generate before repeating

        value: int
        """
        self._properties['count'] = value

    @property
    def values(self):
        """values getter

        TBD

        Returns: list[str]
        """
        return self._properties['values']

    @values.setter
    def values(self, value):
        """values setter

        TBD

        value: list[str]
        """
        self._properties['values'] = value
