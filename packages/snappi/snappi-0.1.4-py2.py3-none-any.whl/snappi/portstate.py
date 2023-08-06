from .snappicommon import SnappiObject


class PortState(SnappiObject):
    def __init__(self, name=None, link=None, capture=None):
        super(PortState, self).__init__()
        self.name = name
        self.link = link
        self.capture = capture

    @property
    def name(self):
        """name getter

        TBD

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        TBD

        value: str
        """
        self._properties['name'] = value

    @property
    def link(self):
        """link getter

        TBD

        Returns: Union[up, down]
        """
        return self._properties['link']

    @link.setter
    def link(self, value):
        """link setter

        TBD

        value: Union[up, down]
        """
        self._properties['link'] = value

    @property
    def capture(self):
        """capture getter

        TBD

        Returns: Union[started, stopped]
        """
        return self._properties['capture']

    @capture.setter
    def capture(self, value):
        """capture setter

        TBD

        value: Union[started, stopped]
        """
        self._properties['capture'] = value
