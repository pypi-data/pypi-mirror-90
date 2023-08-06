from .snappicommon import SnappiObject


class CaptureMacAddressFilter(SnappiObject):
    def __init__(self, mac=None, filter=None, mask=None):
        super(CaptureMacAddressFilter, self).__init__()
        self.mac = mac
        self.filter = filter
        self.mask = mask

    @property
    def mac(self):
        """mac getter

        The type of mac address filters. This can be either source or destination.

        Returns: Union[source, destination]
        """
        return self._properties['mac']

    @mac.setter
    def mac(self, value):
        """mac setter

        The type of mac address filters. This can be either source or destination.

        value: Union[source, destination]
        """
        self._properties['mac'] = value

    @property
    def filter(self):
        """filter getter

        The value of the mac address.

        Returns: str
        """
        return self._properties['filter']

    @filter.setter
    def filter(self, value):
        """filter setter

        The value of the mac address.

        value: str
        """
        self._properties['filter'] = value

    @property
    def mask(self):
        """mask getter

        The value of the mask to be applied to the mac address.

        Returns: str
        """
        return self._properties['mask']

    @mask.setter
    def mask(self, value):
        """mask setter

        The value of the mask to be applied to the mac address.

        value: str
        """
        self._properties['mask'] = value
