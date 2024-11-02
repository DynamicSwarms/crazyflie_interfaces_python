from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from std_msgs.msg import String

from typing import Callable


class ConsoleClient:
    def __init__(self, node: Node, prefix: str, callback: Callable[[str], None] = None):
        """Initializes a Console client.

        Pass a callback in order to receive message Strings sent from the crazyflie

        Args:
            node (Node): A rclpy Node to attach the subscriber to
            prefix (str): The ros prefix for the crazyflie (e.g. cfXX)
            callback (Callable[[str],]): A callback which gets called when a message gets received
        """
        self.message_callback = callback
        callback_group = MutuallyExclusiveCallbackGroup()
        qos_profile = 10

        node.create_subscription(
            String,
            prefix + "/console",
            self._console_callback,
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

    def _console_callback(self, msg: String) -> None:
        message = msg.data
        if self.message_callback:
            self.message_callback(message)
