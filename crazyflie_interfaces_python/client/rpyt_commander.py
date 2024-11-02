from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup


class RPYTCommanderClient:

    def __init__(self, node: Node, prefix: str):
        callback_group = MutuallyExclusiveCallbackGroup
        qos_profile = 10

        # self.rpyt_publisher = node.create_publisher(
        #    RPYT,
        #    "~/send_setpoint",
        #    qos_profile=qos_profile,
        #    callback_group=callback_group,
        # )

    def send_rpyt_setpoint(
        self, roll: float, pitch: float, yawrate: float, thrust: int
    ) -> None:
        raise NotImplementedError("There is currently no rpyt support in this library.")
