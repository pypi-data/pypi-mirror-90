from .snappicommon import SnappiObject


class LagStatic(SnappiObject):
    _TYPES = {
        'lag_id': '.devicepattern.DevicePattern',
    }

    def __init__(self):
        super(LagStatic, self).__init__()

    @property
    def lag_id(self):
        """lag_id getter

        A container for emulated device property patterns.The static lag id.

        Returns: obj(snappi.DevicePattern)
        """
        from .devicepattern import DevicePattern
        if 'lag_id' not in self._properties or self._properties['lag_id'] is None:
            self._properties['lag_id'] = DevicePattern()
        return self._properties['lag_id']
