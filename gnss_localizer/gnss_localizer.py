# This program send the GNSS data to the ekf_localizer node
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped

import carla
from tf2_ros.transform_listener import TransformListener
from tf2_ros.buffer import Buffer
import tf_transformations as tf

import time
import math

class GnssLocalizer(Node):
    def __init__(self):
        super().__init__("gnss_localizer")
        # self.sub_topic_ = "/sensing/gnss/pose_with_covariance"

        self.client = carla.Client("localhost", 2000)
        self.client.set_timeout(5.0)
        self.world = self.client.get_world()

        self.agent_role_name = "hero"
        time.sleep(1)
        self.ego_vehicle = self.get_agent_actor(self.world, self.agent_role_name)


        self.pub_topic_ = "/localization/pose_estimator/gnss/pose_with_covariance"
        # self.sub_ = self.create_subscription(
        #     PoseWithCovarianceStamped, 
        #     self.sub_topic_, 
        #     self.gnss_callback, 
        #     10)

        self.pub_ = self.create_publisher(
            PoseWithCovarianceStamped, 
            self.pub_topic_, 
            10)
        
        self.timer_ = self.create_timer(0.1, self.gnss_callback)
    
    def gnss_callback(self):
        output_msg = PoseWithCovarianceStamped()

        output_msg.header.frame_id = "map"
        output_msg.header.stamp = self.get_clock().now().to_msg()
        # msg.pose.pose.position.x -= 1.0
        # msg.pose.covariance = [
        # 0.01, 0.0, 0.0,  0.0,  0.0,  0.0,
        # 0.0, 0.01, 0.0,  0.0,  0.0,  0.0,
        # 0.0, 0.0, 0.01, 0.0,  0.0,  0.0,
        # 0.0, 0.0, 0.0,  0.01, 0.0,  0.0,
        # 0.0, 0.0, 0.0,  0.0,  0.01, 0.0,
        # 0.0, 0.0, 0.0,  0.0,  0.0,  0.01,
        # ]

        output_msg.pose.pose.position.x = self.ego_vehicle.get_location().x
        output_msg.pose.pose.position.y = self.ego_vehicle.get_location().y * (-1.0)
        output_msg.pose.pose.position.z = self.ego_vehicle.get_location().z

        roll_ = self.ego_vehicle.get_transform().rotation.roll
        pitch_ = self.ego_vehicle.get_transform().rotation.pitch
        yaw_ = self.ego_vehicle.get_transform().rotation.yaw * (-1.0)

        roll_ = math.radians(roll_)
        pitch_ = math.radians(pitch_)
        yaw_ = math.radians(yaw_)

        orientation = tf.quaternion_from_euler(
            roll_, pitch_, yaw_
            )
        
        output_msg.pose.pose.orientation.x = orientation[0]
        output_msg.pose.pose.orientation.y = orientation[1]
        output_msg.pose.pose.orientation.z = orientation[2]
        output_msg.pose.pose.orientation.w = orientation[3]
        
        output_msg.pose.covariance = [
        0.001, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.001, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.001, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.001, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.001, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.001,
        ]
        self.pub_.publish(output_msg)
    
    def get_agent_actor(self, world, role_name):
            actors = None
            actors = world.get_actors()
            for car in actors:
                if car.attributes['role_name'] == role_name:
                    return car
            return None


def main():
    rclpy.init()
    node = GnssLocalizer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
