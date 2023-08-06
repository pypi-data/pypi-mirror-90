from .snappicommon import SnappiObject


class DeviceCounter(SnappiObject):
    def __init__(self, start=None, step=None):
        super(DeviceCounter, self).__init__()
        self.start = start
        self.step = step

    @property
    def start(self):
        """start getter

        TBD

        Returns: str
        """
        return self._properties['start']

    @start.setter
    def start(self, value):
        """start setter

        TBD

        value: str
        """
        self._properties['start'] = value

    @property
    def step(self):
        """step getter

        TBD

        Returns: str
        """
        return self._properties['step']

    @step.setter
    def step(self, value):
        """step setter

        TBD

        value: str
        """
        self._properties['step'] = value
