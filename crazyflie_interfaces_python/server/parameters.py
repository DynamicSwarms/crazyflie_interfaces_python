from abc import ABC, abstractmethod

from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import Empty

from typing import List


class ParametersServer(ABC):
    def __init__(self, node: Node):
        self.node = node
        callback_group = MutuallyExclusiveCallbackGroup()
        node.create_subscription(
            Empty,
            "~/download_parameters_toc",
            self._download_toc,
            10,
            callback_group=callback_group,
        )

        node.create_subscription(
            Empty,
            "~/get_parameters_toc_info",
            self._get_toc_info,
            10,
            callback_group=callback_group,
        )

        node.add_on_set_parameters_callback(self._set_parameter_callback)

    def initalize_parameters(self, parameters: List[dict]):
        for parameter in parameters:
            group = parameter.group
            name = parameter.name
            type = parameter.type
            self.node.declare_parameter(str(group) + "." + str(name), type)

    @abstractmethod
    def download_toc(self) -> None:
        pass

    @abstractmethod
    def get_toc_info(self) -> None:
        pass

    @abstractmethod
    def set_parameter(self, group: str, name: str, value: Parameter.Type):
        """This gets called if a parameter is set through ros

        Set the parameter in crazyflie appropriately

        Args:
            group (str): _description_
            name (str): _description_
            value (Parameter.Type): _description_
        """
        pass

    def _download_toc(self, msg: Empty) -> None:
        self.download_toc()

    def _get_toc_info(self, msg: Empty) -> None:
        self.get_toc_info()

    def _set_parameter_callback(self, params: List[Parameter]) -> SetParametersResult:
        for param in params:
            group, name = param.name.split(".")
            self.set_parameter(group, name, param.value)
