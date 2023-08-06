from .snappicommon import SnappiObject


class FlowSizeIncrement(SnappiObject):
    def __init__(self, start=None, end=None, step=None):
        super(FlowSizeIncrement, self).__init__()
        self.start = start
        self.end = end
        self.step = step

    @property
    def start(self):
        """start getter

        Starting frame size in bytes

        Returns: int
        """
        return self._properties['start']

    @start.setter
    def start(self, value):
        """start setter

        Starting frame size in bytes

        value: int
        """
        self._properties['start'] = value

    @property
    def end(self):
        """end getter

        Ending frame size in bytes

        Returns: int
        """
        return self._properties['end']

    @end.setter
    def end(self, value):
        """end setter

        Ending frame size in bytes

        value: int
        """
        self._properties['end'] = value

    @property
    def step(self):
        """step getter

        Step frame size in bytes

        Returns: int
        """
        return self._properties['step']

    @step.setter
    def step(self, value):
        """step setter

        Step frame size in bytes

        value: int
        """
        self._properties['step'] = value
