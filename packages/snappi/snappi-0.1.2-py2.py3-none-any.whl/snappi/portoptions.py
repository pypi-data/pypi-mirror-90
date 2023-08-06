from .snappicommon import SnappiObject


class PortOptions(SnappiObject):
    def __init__(self, location_preemption=None):
        super(PortOptions, self).__init__()
        self.location_preemption = location_preemption

    @property
    def location_preemption(self):
        """location_preemption getter

        Preempt all the test port locations as defined by the Port.Port.properties.location. If the test ports defined by their location values are in use and this value is true, the test ports will be preempted.

        Returns: boolean
        """
        return self._properties['location_preemption']

    @location_preemption.setter
    def location_preemption(self, value):
        """location_preemption setter

        Preempt all the test port locations as defined by the Port.Port.properties.location. If the test ports defined by their location values are in use and this value is true, the test ports will be preempted.

        value: boolean
        """
        self._properties['location_preemption'] = value
