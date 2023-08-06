from .snappicommon import SnappiObject


class Bgpv4Metric(SnappiObject):
    def __init__(self, name=None, sessions_total=None, sessions_up=None, sessions_down=None, sessions_not_started=None, routes_advertised=None, routes_withdrawn=None):
        super(Bgpv4Metric, self).__init__()
        self.name = name
        self.sessions_total = sessions_total
        self.sessions_up = sessions_up
        self.sessions_down = sessions_down
        self.sessions_not_started = sessions_not_started
        self.routes_advertised = routes_advertised
        self.routes_withdrawn = routes_withdrawn

    @property
    def name(self):
        """name getter

        The name of a configured BGPv4 Object.

        Returns: str
        """
        return self._properties['name']

    @name.setter
    def name(self, value):
        """name setter

        The name of a configured BGPv4 Object.

        value: str
        """
        self._properties['name'] = value

    @property
    def sessions_total(self):
        """sessions_total getter

        Total number of session

        Returns: int
        """
        return self._properties['sessions_total']

    @sessions_total.setter
    def sessions_total(self, value):
        """sessions_total setter

        Total number of session

        value: int
        """
        self._properties['sessions_total'] = value

    @property
    def sessions_up(self):
        """sessions_up getter

        Sessions are in active state

        Returns: int
        """
        return self._properties['sessions_up']

    @sessions_up.setter
    def sessions_up(self, value):
        """sessions_up setter

        Sessions are in active state

        value: int
        """
        self._properties['sessions_up'] = value

    @property
    def sessions_down(self):
        """sessions_down getter

        Sessions are not active state

        Returns: int
        """
        return self._properties['sessions_down']

    @sessions_down.setter
    def sessions_down(self, value):
        """sessions_down setter

        Sessions are not active state

        value: int
        """
        self._properties['sessions_down'] = value

    @property
    def sessions_not_started(self):
        """sessions_not_started getter

        Sessions not able to start due to some internal issue

        Returns: int
        """
        return self._properties['sessions_not_started']

    @sessions_not_started.setter
    def sessions_not_started(self, value):
        """sessions_not_started setter

        Sessions not able to start due to some internal issue

        value: int
        """
        self._properties['sessions_not_started'] = value

    @property
    def routes_advertised(self):
        """routes_advertised getter

        Number of advertised routes sent

        Returns: int
        """
        return self._properties['routes_advertised']

    @routes_advertised.setter
    def routes_advertised(self, value):
        """routes_advertised setter

        Number of advertised routes sent

        value: int
        """
        self._properties['routes_advertised'] = value

    @property
    def routes_withdrawn(self):
        """routes_withdrawn getter

        Number of routes withdrawn

        Returns: int
        """
        return self._properties['routes_withdrawn']

    @routes_withdrawn.setter
    def routes_withdrawn(self, value):
        """routes_withdrawn setter

        Number of routes withdrawn

        value: int
        """
        self._properties['routes_withdrawn'] = value
