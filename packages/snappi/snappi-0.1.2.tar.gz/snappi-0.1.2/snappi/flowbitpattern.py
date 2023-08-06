from .snappicommon import SnappiObject


class FlowBitPattern(SnappiObject):
    _TYPES = {
        'bitlist': '.flowbitlist.FlowBitList',
        'bitcounter': '.flowbitcounter.FlowBitCounter',
    }

    def __init__(self):
        super(FlowBitPattern, self).__init__()

    @property
    def bitlist(self):
        from .flowbitlist import FlowBitList
        if 'bitlist' not in self._properties or self._properties['bitlist'] is None:
            self._properties['bitlist'] = FlowBitList()
        self.choice = 'bitlist'
        return self._properties['bitlist']

    @property
    def bitcounter(self):
        from .flowbitcounter import FlowBitCounter
        if 'bitcounter' not in self._properties or self._properties['bitcounter'] is None:
            self._properties['bitcounter'] = FlowBitCounter()
        self.choice = 'bitcounter'
        return self._properties['bitcounter']

    @property
    def choice(self):
        """choice getter

        TBD

        Returns: Union[bitlist, bitcounter, choice, choice, choice]
        """
        return self._properties['choice']

    @choice.setter
    def choice(self, value):
        """choice setter

        TBD

        value: Union[bitlist, bitcounter, choice, choice, choice]
        """
        self._properties['choice'] = value
