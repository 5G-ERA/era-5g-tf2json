import time
from typing import List

import numpy  # noqa
import rclpy  # pants: no-infer-dep
from geometry_msgs.msg import TransformStamped  # pants: no-infer-dep
from rclpy.node import Node  # pants: no-infer-dep
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster  # pants: no-infer-dep

from era_5g_tf2json.tf2_web_republisher import TFRepublisher

t = TransformStamped()
t.header.frame_id = "world"
t.child_frame_id = "robot"


def test_republisher() -> None:

    received_transforms: List[List[TransformStamped]] = []

    def callback(transforms: List[TransformStamped]) -> None:
        received_transforms.append(transforms)

    rclpy.init()

    node = Node("republisher_test_node")

    t.header.stamp = node.get_clock().now().to_msg()

    tf_static_broadcaster = StaticTransformBroadcaster(node)
    tf_static_broadcaster.sendTransform(t)

    republisher = TFRepublisher(node, callback, 1.0)
    republisher.subscribe_transform(t.child_frame_id, t.header.frame_id, 1.0, 1.0, 0.0)

    start_time = time.monotonic()

    while time.monotonic() - 5.0 < start_time:
        rclpy.spin_once(node)
        time.sleep(0.01)

    assert len(received_transforms) == 1
    assert len(received_transforms[0]) == 1
    assert received_transforms[0][0].header.frame_id == t.header.frame_id
    assert received_transforms[0][0].child_frame_id == t.child_frame_id

    rclpy.shutdown()


def test_republisher_periodic() -> None:

    received_transforms: List[List[TransformStamped]] = []

    def callback(transforms: List[TransformStamped]) -> None:
        received_transforms.append(transforms)

    rclpy.init()

    node = Node("republisher_test_node")

    t.header.stamp = node.get_clock().now().to_msg()

    tf_static_broadcaster = StaticTransformBroadcaster(node)
    tf_static_broadcaster.sendTransform(t)

    republisher = TFRepublisher(node, callback, 1.0)
    republisher.subscribe_transform(t.child_frame_id, t.header.frame_id, 1.0, 1.0, 1.0)

    start_time = time.monotonic()

    while time.monotonic() - 5.0 < start_time:
        rclpy.spin_once(node)
        time.sleep(0.01)

    assert len(received_transforms) > 2
    assert len(received_transforms[0]) == 1
    assert received_transforms[0][0].header.frame_id == t.header.frame_id
    assert received_transforms[0][0].child_frame_id == t.child_frame_id

    rclpy.shutdown()
