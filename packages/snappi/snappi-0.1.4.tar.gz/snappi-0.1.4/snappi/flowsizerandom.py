from .snappicommon import SnappiObject


class FlowSizeRandom(SnappiObject):
    def __init__(self, min=None, max=None):
        super(FlowSizeRandom, self).__init__()
        self.min = min
        self.max = max

    @property
    def min(self):
        """min getter

        TBD

        Returns: int
        """
        return self._properties['min']

    @min.setter
    def min(self, value):
        """min setter

        TBD

        value: int
        """
        self._properties['min'] = value

    @property
    def max(self):
        """max getter

        TBD

        Returns: int
        """
        return self._properties['max']

    @max.setter
    def max(self, value):
        """max setter

        TBD

        value: int
        """
        self._properties['max'] = value
