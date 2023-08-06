from .snappicommon import SnappiObject


class FlowMetricsRequest(SnappiObject):
    def __init__(self, flow_names=None, column_names=None, result_group_names=None):
        super(FlowMetricsRequest, self).__init__()
        self.flow_names = flow_names
        self.column_names = column_names
        self.result_group_names = result_group_names

    @property
    def flow_names(self):
        """flow_names getter

        The names of flow objects to return results for. An empty list will return results for all flows.

        Returns: list[str]
        """
        return self._properties['flow_names']

    @flow_names.setter
    def flow_names(self, value):
        """flow_names setter

        The names of flow objects to return results for. An empty list will return results for all flows.

        value: list[str]
        """
        self._properties['flow_names'] = value

    @property
    def column_names(self):
        """column_names getter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the flow cannot be excluded.

        Returns: list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss]]
        """
        return self._properties['column_names']

    @column_names.setter
    def column_names(self, value):
        """column_names setter

        The list of column names that the returned result set will contain. If the list is empty then all columns will be returned except for any result_groups. The name of the flow cannot be excluded.

        value: list[Union[transmit, port_tx, port_rx, frames_tx, frames_rx, bytes_tx, bytes_rx, frames_tx_rate, frames_rx_rate, loss]]
        """
        self._properties['column_names'] = value

    @property
    def result_group_names(self):
        """result_group_names getter

        Extend the details of flow results by specifying any configured flow packet header field result_group names.

        Returns: list[str]
        """
        return self._properties['result_group_names']

    @result_group_names.setter
    def result_group_names(self, value):
        """result_group_names setter

        Extend the details of flow results by specifying any configured flow packet header field result_group names.

        value: list[str]
        """
        self._properties['result_group_names'] = value
