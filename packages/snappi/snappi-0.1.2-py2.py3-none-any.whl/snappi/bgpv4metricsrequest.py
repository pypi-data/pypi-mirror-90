from .snappicommon import SnappiObject


class Bgpv4MetricsRequest(SnappiObject):
    def __init__(self, names=None):
        super(Bgpv4MetricsRequest, self).__init__()
        self.names = names

    @property
    def names(self):
        """names getter

        The names of BGP objects to return results for. An empty list will return results for all BGP.

        Returns: list[str]
        """
        return self._properties['names']

    @names.setter
    def names(self, value):
        """names setter

        The names of BGP objects to return results for. An empty list will return results for all BGP.

        value: list[str]
        """
        self._properties['names'] = value
