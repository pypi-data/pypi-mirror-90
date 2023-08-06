from .snappicommon import SnappiObject


class FlowCounter(SnappiObject):
    def __init__(self, start=None, step=None, count=None):
        super(FlowCounter, self).__init__()
        self.start = start
        self.step = step
        self.count = count

    @property
    def start(self):
        """start getter

        The value at which the pattern will start.

        Returns: Union[string,number]
        """
        return self._properties['start']

    @start.setter
    def start(self, value):
        """start setter

        The value at which the pattern will start.

        value: Union[string,number]
        """
        self._properties['start'] = value

    @property
    def step(self):
        """step getter

        The value at which the pattern will increment or decrement by.

        Returns: Union[string,number]
        """
        return self._properties['step']

    @step.setter
    def step(self, value):
        """step setter

        The value at which the pattern will increment or decrement by.

        value: Union[string,number]
        """
        self._properties['step'] = value

    @property
    def count(self):
        """count getter

        The number of values in the pattern.

        Returns: float
        """
        return self._properties['count']

    @count.setter
    def count(self, value):
        """count setter

        The number of values in the pattern.

        value: float
        """
        self._properties['count'] = value
