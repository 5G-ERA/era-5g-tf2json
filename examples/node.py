from typing import List

import rclpy  # pants: no-infer-dep
from geometry_msgs.msg import TransformStamped  # pants: no-infer-dep
from rclpy.node import Node  # pants: no-infer-dep

from era_5g_tf2json.tf2_web_republisher import TFRepublisher


class ExampleNode(Node):
    def __init__(self) -> None:
        super(ExampleNode, self).__init__("tf2_web_republisher_example_node")
        self.republisher = TFRepublisher(self, self.callback, 1.0)

    def callback(self, transforms: List[TransformStamped]) -> None:
        self.get_logger().info(f"Got {len(transforms)}")


def main(args=None) -> None:
    rclpy.init(args=args)

    node = ExampleNode()
    node.republisher.subscribe_transform("robot", "world", 0.1, 0.001)
    node.republisher.subscribe_transform("camera", "world", 0.1, 0.001)
    rclpy.spin(node)


if __name__ == "__main__":
    main()
