from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

from builtin_interfaces.msg import Duration
from geometry_msgs.msg import Point
from crazyflie_interfaces.msg import (
    SetGroupMask,
    Takeoff,
    Land,
    Stop,
    GoTo,
    StartTrajectory,
    UploadTrajectory,
    TakeoffWithVelocity,
    LandWithVelocity,
    Spiral,
    TrajectoryPolynomialPiece,
)

from typing import List


class HighLevelCommanderClient:

    def __init__(self, node: Node, prefix: str):
        callback_group = MutuallyExclusiveCallbackGroup()
        qos_profile = 10

        self.set_group_mask_publisher = node.create_publisher(
            SetGroupMask,
            prefix + "/set_group_mask",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.takeoff_publisher = node.create_publisher(
            Takeoff,
            prefix + "/takeoff",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.land_publisher = node.create_publisher(
            Land,
            prefix + "/land",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.stop_publisher = node.create_publisher(
            Stop,
            prefix + "/stop",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.goto_publisher = node.create_publisher(
            GoTo,
            prefix + "/go_to",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.start_trajectory_publisher = node.create_publisher(
            StartTrajectory,
            prefix + "/start_trajectory",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.upload_trajectory_publisher = node.create_publisher(
            UploadTrajectory,
            prefix + "/upload_trajectory",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.takeoff_with_velocity_publisher = node.create_publisher(
            TakeoffWithVelocity,
            prefix + "/takeoff_with_velocity",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.land_with_velocity_publisher = node.create_publisher(
            LandWithVelocity,
            prefix + "/land_with_velocity",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

        self.spiral_publisher = node.create_publisher(
            Spiral,
            prefix + "/spiral",
            qos_profile=qos_profile,
            callback_group=callback_group,
        )

    def set_group_mask(self, group_mask: int):
        """Sets the group mask of the crazyflie

        Deprecated will be removed December 2024

        Args:
            group_mask (int): the group ID this CF belongs to
        """
        msg = SetGroupMask()
        msg.group_mask = group_mask
        self.set_group_mask_publisher.publish(msg)

    def takeoff(
        self,
        target_height: float,
        duration_seconds: float,
        yaw: float = None,
        group_mask: int = 0,
    ) -> None:
        """Vertical takeoff from current x-y position to given height

        The Crazyflie will hover indefinetely after target_height is reached.
        Asynchronous; returns immediately.

        Args:
            target_height (float): height to takeoff to (absolute) in meters
            duration_seconds (float): time it should take until target_height is reached in seconds
            group_mask (int, optional): mask for which CFs this should apply to. Defaults to 0.
        """
        msg = Takeoff()
        msg.group_mask = group_mask
        msg.height = target_height
        msg.use_current_yaw = yaw is None
        if not msg.use_current_yaw:
            msg.yaw = yaw
        msg.duration = self.__seconds_to_duration(duration_seconds)
        self.takeoff_publisher.publish(msg)

    def land(
        self,
        target_height: float,
        duration_seconds: float,
        yaw: float = None,
        group_mask: int = 0,
    ) -> None:
        """Vertical landing from current x-y position to given height

        The Crazyflie will hover indefinetely after target_height is reached.
        # TODO: Do we need to hint for a call to stop?
        Asynchronous; returns immediately.

        Args:
            target_height (float): _description_
            duration_seconds (float): _description_
            yaw (float, optional): _description_. Defaults to None.
            group_mask (int, optional): _description_. Defaults to 0.
        """
        msg = Land()
        msg.group_mask = group_mask
        msg.height = target_height
        msg.use_current_yaw = yaw is None
        if not msg.use_current_yaw:
            msg.yaw = yaw
        msg.duration = self.__seconds_to_duration(duration_seconds)
        self.land_publisher.publish(msg)

    def stop(self, group_mask: int = 0) -> None:
        """Turns off the motors

        Args:
            group_mask (int, optional): mask for which CFs this should apply to. Defaults to 0.
        """
        msg = Stop()
        msg.group_mask = group_mask
        self.stop_publisher.publish(msg)

    def go_to(
        self,
        x: float,
        y: float,
        z: float,
        yaw: float,
        duration_seconds: float,
        relative: bool = False,
        linear: bool = False,
        group_mask: int = 0,
    ) -> None:
        """Move to x, y, z, yaw in duration_seconds amount of time

        The Crazyflie will hover indefinetely afterwards.
        Asynchronous; returns immediately.

        Args:
            x (float): x-position of goal in meters
            y (float): y-position of goal in meters
            z (float): z-position of goal in meters
            yaw (float): target yaw in radians
            duration_seconds (float): Time in seconds it should take the CF to move to goal
            relative (bool, optional): If true the goal and yaw are interpreted as relative to current position. Defaults to False.
            linear (bool, optional): If true a linear interpolation is used for trajectory instead of a smooth polynomial . Defaults to False.
            group_mask (int, optional): mask for which CFs this should apply to. Defaults to 0.
        """
        msg = GoTo()
        msg.group_mask = group_mask
        msg.goal = Point(x, y, z)
        msg.yaw = yaw
        msg.relative = relative
        msg.linear = linear
        msg.duration = self.__seconds_to_duration(duration_seconds)

    def start_trajectory(
        self,
        trajectory_id: int,
        timescale: float = 1.0,
        reversed: bool = False,
        relative: bool = True,
        group_mask: int = 0,
    ) -> None:
        msg = StartTrajectory()
        msg.group_mask = group_mask
        msg.trajectory_id = trajectory_id
        msg.timescale = timescale
        msg.reversed = reversed
        msg.relative = relative
        self.start_trajectory_publisher.publish(msg)

    def upload_trajectory(
        self, trajectory_id: int, piece_offset: int, pieces: List
    ) -> None:
        """_summary_

        TODO: How do poly pieces work, should we also use uav_trajectory.py

        Args:
            trajectory_id (int): _description_
            piece_offset (int): _description_
            pieces (List): _description_
        """
        msg = UploadTrajectory()
        msg.trajectory_id = trajectory_id
        msg.piece_offset = piece_offset
        for _piece in pieces:
            piece = TrajectoryPolynomialPiece()
            piece.duration = self.__seconds_to_duration(_piece.duration_seconds)
            piece.poly_x = _piece.poly_x
            piece.poly_y = _piece.poly_y
            piece.poly_z = _piece.poly_z
            piece.poly_yaw = _piece.poly_yaw
            msg.pieces.append(piece)
        self.upload_trajectory_publisher.publish(msg)

    def takeoff_with_velocity(
        self,
        height: float,
        yaw: float,
        velocity: float,
        height_is_relative: bool = False,
        use_current_yaw: bool = False,
        group_mask: int = 0,
    ) -> None:
        msg = TakeoffWithVelocity()
        msg.group_mask = group_mask
        msg.height = height
        msg.height_is_relative = height_is_relative
        msg.yaw = yaw
        msg.velocity = velocity
        msg.use_current_yaw = use_current_yaw
        self.takeoff_with_velocity_publisher.publish(msg)

    def land_with_velocity(
        self,
        height: float,
        yaw: float,
        velocity: float,
        height_is_relative: bool = False,
        use_current_yaw: bool = False,
        group_mask: int = 0,
    ) -> None:
        msg = LandWithVelocity()
        msg.group_mask = group_mask
        msg.height = height
        msg.height_is_relative = height_is_relative
        msg.yaw = yaw
        msg.use_current_yaw = use_current_yaw
        msg.velocity = velocity
        self.land_with_velocity_publisher.publish(msg)

    def spiral(
        self,
        sideways: bool,
        clockwise: bool,
        phi: float,
        r0: float,
        rf: float,
        dz: float,
        duration_seconds: float,
        group_mask: int = 0,
    ) -> None:
        msg = Spiral()
        msg.group_mask = group_mask
        msg.sideways = sideways
        msg.clockwise = clockwise
        msg.phi = phi
        msg.r0 = r0
        msg.rf = rf
        msg.dz = dz
        msg.duration = self.__seconds_to_duration(duration_seconds)
        self.spiral_publisher.publish(msg)

    def __seconds_to_duration(self, seconds: float) -> Duration:
        i_seconds = int(seconds)
        fractional_seconds = seconds - i_seconds
        nanoseconds = int(fractional_seconds * 1_000_000_000)
        return Duration(i_seconds, nanoseconds)
