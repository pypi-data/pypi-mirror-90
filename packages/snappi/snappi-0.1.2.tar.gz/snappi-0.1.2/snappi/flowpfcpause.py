from .snappicommon import SnappiObject


class FlowPfcPause(SnappiObject):
    _TYPES = {
        'dst': '.flowpattern.FlowPattern',
        'src': '.flowpattern.FlowPattern',
        'ether_type': '.flowpattern.FlowPattern',
        'control_op_code': '.flowpattern.FlowPattern',
        'class_enable_vector': '.flowpattern.FlowPattern',
        'pause_class_0': '.flowpattern.FlowPattern',
        'pause_class_1': '.flowpattern.FlowPattern',
        'pause_class_2': '.flowpattern.FlowPattern',
        'pause_class_3': '.flowpattern.FlowPattern',
        'pause_class_4': '.flowpattern.FlowPattern',
        'pause_class_5': '.flowpattern.FlowPattern',
        'pause_class_6': '.flowpattern.FlowPattern',
        'pause_class_7': '.flowpattern.FlowPattern',
    }

    def __init__(self):
        super(FlowPfcPause, self).__init__()

    @property
    def dst(self):
        """dst getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'dst' not in self._properties or self._properties['dst'] is None:
            self._properties['dst'] = FlowPattern()
        return self._properties['dst']

    @property
    def src(self):
        """src getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'src' not in self._properties or self._properties['src'] is None:
            self._properties['src'] = FlowPattern()
        return self._properties['src']

    @property
    def ether_type(self):
        """ether_type getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'ether_type' not in self._properties or self._properties['ether_type'] is None:
            self._properties['ether_type'] = FlowPattern()
        return self._properties['ether_type']

    @property
    def control_op_code(self):
        """control_op_code getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'control_op_code' not in self._properties or self._properties['control_op_code'] is None:
            self._properties['control_op_code'] = FlowPattern()
        return self._properties['control_op_code']

    @property
    def class_enable_vector(self):
        """class_enable_vector getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'class_enable_vector' not in self._properties or self._properties['class_enable_vector'] is None:
            self._properties['class_enable_vector'] = FlowPattern()
        return self._properties['class_enable_vector']

    @property
    def pause_class_0(self):
        """pause_class_0 getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'pause_class_0' not in self._properties or self._properties['pause_class_0'] is None:
            self._properties['pause_class_0'] = FlowPattern()
        return self._properties['pause_class_0']

    @property
    def pause_class_1(self):
        """pause_class_1 getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'pause_class_1' not in self._properties or self._properties['pause_class_1'] is None:
            self._properties['pause_class_1'] = FlowPattern()
        return self._properties['pause_class_1']

    @property
    def pause_class_2(self):
        """pause_class_2 getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'pause_class_2' not in self._properties or self._properties['pause_class_2'] is None:
            self._properties['pause_class_2'] = FlowPattern()
        return self._properties['pause_class_2']

    @property
    def pause_class_3(self):
        """pause_class_3 getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'pause_class_3' not in self._properties or self._properties['pause_class_3'] is None:
            self._properties['pause_class_3'] = FlowPattern()
        return self._properties['pause_class_3']

    @property
    def pause_class_4(self):
        """pause_class_4 getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'pause_class_4' not in self._properties or self._properties['pause_class_4'] is None:
            self._properties['pause_class_4'] = FlowPattern()
        return self._properties['pause_class_4']

    @property
    def pause_class_5(self):
        """pause_class_5 getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'pause_class_5' not in self._properties or self._properties['pause_class_5'] is None:
            self._properties['pause_class_5'] = FlowPattern()
        return self._properties['pause_class_5']

    @property
    def pause_class_6(self):
        """pause_class_6 getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'pause_class_6' not in self._properties or self._properties['pause_class_6'] is None:
            self._properties['pause_class_6'] = FlowPattern()
        return self._properties['pause_class_6']

    @property
    def pause_class_7(self):
        """pause_class_7 getter

        A container for packet header field patterns.

        Returns: obj(snappi.FlowPattern)
        """
        from .flowpattern import FlowPattern
        if 'pause_class_7' not in self._properties or self._properties['pause_class_7'] is None:
            self._properties['pause_class_7'] = FlowPattern()
        return self._properties['pause_class_7']
