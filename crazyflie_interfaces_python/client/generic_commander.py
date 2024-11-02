from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from geometry_msgs.msg import Vector3, Pose, Twist, Point, Quaternion
from crazyflie_interfaces.msg import (
    NotifySetpointsStop,
    VelocityWorld,
    Hover,
    FullState,
    Position,
)

from typing import List


class GenericCommanderClient:

    def __init__(self, node: Node, prefix: str):
        callback_group = MutuallyExclusiveCallbackGroup()
        qos_profile = 10  # Should this be passed?

        self.notify_setpoints_stop_publisher = node.create_publisher(
            NotifySetpointsStop,
            prefix + "/notify_setpoints_stop",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.velocity_world_publisher = node.create_publisher(
            VelocityWorld,
            prefix + "/cmd_vel",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.hover_publisher = node.create_publisher(
            Hover,
            prefix + "/cmd_hover",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.full_state_publisher = node.create_publisher(
            FullState,
            prefix + "/cmd_full_state",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.position_publisher = node.create_publisher(
            Position,
            prefix + "/cmd_position",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

    def notify_setpoints_stop(
        self, remain_valid_milliseconds: int = 100, group_mask: int = 0
    ) -> None:
        """Sends a notify setpoints command

        Args:
            remain_valid_milliseconds (int, optional): _description_. Defaults to 100.
            group_mask (int, optional): _description_. Defaults to 0.
        """
        msg = NotifySetpointsStop()
        msg.group_mask = group_mask
        msg.remain_valid_millisecs = remain_valid_milliseconds
        self.notify_setpoints_stop_publisher.publish(msg)

    def cmd_velocity_world(self, velocity: List[float], yawrate: float = 0.0) -> None:
        """

        Args:
            velocity (List[float]): _description_
            yawrate (float, optional): _description_. Defaults to 0.0.
        """
        msg = VelocityWorld()
        x, y, z = velocity
        msg.vel = Vector3(x, y, z)
        msg.yaw_rate = yawrate
        self.velocity_world_publisher.publish(msg)

    def cmd_hover(
        self,
        z_distance: float,
        velocity_x: float = 0.0,
        velocity_y: float = 0.0,
        yawrate: float = 0.0,
    ) -> None:
        """Send a hover command

        Args:
            z_distance (float): _description_
            velocity_x (float, optional): _description_. Defaults to 0.0.
            velocity_y (float, optional): _description_. Defaults to 0.0.
            yawrate (float, optional): _description_. Defaults to 0.0.
        """
        msg = Hover()
        msg.z_distance = z_distance
        msg.vx = velocity_x
        msg.vy = velocity_y
        msg.yawrate = yawrate
        self.hover_publisher.publish(msg)

    def cmd_full_state(
        self,
        position: List[float],
        velocity: List[float],
        acceleration: List[float],
        orientation: List[float],
        angular_rate: List[float],
    ) -> None:
        """Sends a full-state controller setpoint command

        Args:
            position (List[float]): _description_
            velocity (List[float]): _description_
            acceleration (List[float]): _description_
            yaw (float): _description_
            omega (List[float]): _description_
        """
        pose = Pose()
        (pose.position.x, pose.position.y, pose.position.z) = position
        (
            pose.orientation.x,
            pose.orientation.y,
            pose.orientation.z,
            pose.orientation.w,
        ) = orientation

        twist = Twist()
        twist.linear.x, twist.linear.y, twist.linear.z = velocity
        twist.angular.x, twist.angular.y, twist.angular.z = angular_rate

        acceleration = Vector3()
        acceleration.x, acceleration.y, acceleration.z = acceleration

        msg = FullState()
        msg.pose = pose
        msg.twist = twist
        msg.acc = acceleration
        self.full_state_publisher.publish(msg)

    def cmd_position(self, position: List[float], yaw: float) -> None:
        """

        Args:
            position (List[float]): _description_
        """
        msg = Position()
        msg.x, msg.y, msg.z = position
        msg.yaw = yaw
        self.position_publisher.publish(msg)
