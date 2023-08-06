from .snappicommon import SnappiObject


class Capabilities(SnappiObject):
    def __init__(self, unsupported=None, formats=None):
        super(Capabilities, self).__init__()
        self.unsupported = unsupported
        self.formats = formats

    @property
    def unsupported(self):
        """unsupported getter

        A list of /components/schemas/... paths that are not supported.

        Returns: list[str]
        """
        return self._properties['unsupported']

    @unsupported.setter
    def unsupported(self, value):
        """unsupported setter

        A list of /components/schemas/... paths that are not supported.

        value: list[str]
        """
        self._properties['unsupported'] = value

    @property
    def formats(self):
        """formats getter

        A /components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums.

        Returns: list[str]
        """
        return self._properties['formats']

    @formats.setter
    def formats(self, value):
        """formats setter

        A /components/schemas/... path and specific format details regarding the path. Specific model format details can be additional objects and properties represented as a hashmap. For example layer1 models are defined as a hashmap key to object with each object consisting of a specific name/value property pairs. This list of items will detail any specific formats, properties, enums.

        value: list[str]
        """
        self._properties['formats'] = value
