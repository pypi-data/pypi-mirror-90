from .snappicommon import SnappiObject


class FlowState(SnappiObject):
    def __init__(self, name=None, transmit=None):
        super(FlowState, self).__init__()
        self.name = name
        self.transmit = transmit

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
    def transmit(self):
        """transmit getter

        TBD

        Returns: Union[started, stopped, paused]
        """
        return self._properties['transmit']

    @transmit.setter
    def transmit(self, value):
        """transmit setter

        TBD

        value: Union[started, stopped, paused]
        """
        self._properties['transmit'] = value
