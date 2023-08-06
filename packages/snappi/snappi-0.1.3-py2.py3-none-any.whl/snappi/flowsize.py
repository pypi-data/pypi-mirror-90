from .snappicommon import SnappiObject


class FlowSize(SnappiObject):
    _TYPES = {
        'increment': '.flowsizeincrement.FlowSizeIncrement',
        'random': '.flowsizerandom.FlowSizeRandom',
    }

    def __init__(self):
        super(FlowSize, self).__init__()

    @property
    def increment(self):
        from .flowsizeincrement import FlowSizeIncrement
        if 'increment' not in self._properties or self._properties['increment'] is None:
            self._properties['increment'] = FlowSizeIncrement()
        self.choice = 'increment'
        return self._properties['increment']

    @property
    def random(self):
        from .flowsizerandom import FlowSizeRandom
        if 'random' not in self._properties or self._properties['random'] is None:
            self._properties['random'] = FlowSizeRandom()
        self.choice = 'random'
        return self._properties['random']

    @property
    def choice(self):
        """choice getter

        TBD

        Returns: Union[fixed, increment, random, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[fixed, increment, random, choice, choice, choice]
        """
        self._properties['choice'] = value

    @property
    def fixed(self):
        """fixed getter

        TBD

        Returns: int
        """
        return self._properties['fixed']

    @fixed.setter
    def fixed(self, value):
        """fixed setter

        TBD

        value: int
        """
        self._properties['choice'] = 'fixed'
        self._properties['fixed'] = value
