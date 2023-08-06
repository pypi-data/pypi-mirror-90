from .snappicommon import SnappiObject


class ConfigOptions(SnappiObject):
    _TYPES = {
        'port_options': '.portoptions.PortOptions',
    }

    def __init__(self):
        super(ConfigOptions, self).__init__()

    @property
    def port_options(self):
        """port_options getter

        TBD

        Returns: obj(snappi.PortOptions)
        """
        from .portoptions import PortOptions
        if 'port_options' not in self._properties or self._properties['port_options'] is None:
            self._properties['port_options'] = PortOptions()
        return self._properties['port_options']
