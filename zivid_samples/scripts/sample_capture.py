#!/usr/bin/env python

import rospy
import rosnode
import dynamic_reconfigure.client
from zivid_camera.srv import *
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
from std_srvs.srv import Trigger, TriggerResponse


class Sample:
    def __init__(self):
        rospy.init_node("sample_capture_py", anonymous=True)

        rospy.loginfo("Starting sample_capture.py")

        rospy.wait_for_service("/zivid_camera/capture", 30.0)

        rospy.Subscriber("/zivid_camera/points/xyzrgba", PointCloud2, self.on_points)

        self.capture_service = rospy.ServiceProxy("/zivid_camera/capture", Capture)
        self.trigger_service = rospy.Service('/zivid1/trigger', Trigger, self.trigger_response)

        rospy.loginfo("Enabling the reflection filter")
        settings_client = dynamic_reconfigure.client.Client("/zivid_camera/settings/")
        settings_config = {"processing_filters_reflection_removal_enabled": True}
        settings_client.update_configuration(settings_config)

        rospy.loginfo("Enabling and configure the first acquisition")
        acquisition_0_client = dynamic_reconfigure.client.Client(
            "/zivid_camera/settings/acquisition_0"
        )
        acquisition_0_client_color_settings = dynamic_reconfigure.client.Client(
            "/zivid_camera/settings"
        )
        acquisition_0_config = {
            "enabled": True,
            "aperture": 3.67,
            "exposure_time": 50000,
            "gain": 1.0,
            "brightness": 1.0,
        }
        acquisition_0_config_color = {
            "processing_color_balance_blue": 1.29,
            "processing_color_gamma": 0.8,
        }
        acquisition_0_client.update_configuration(acquisition_0_config)
        acquisition_0_client_color_settings.update_configuration(acquisition_0_config_color)

    def capture(self):
        rospy.loginfo("Calling capture service")
        self.capture_service()

    def on_points(self, data):
        rospy.loginfo("PointCloud received")
#        self.capture()

    def trigger_response(self,request):
        self.capture()
        return TriggerResponse(
            success=True,
            message="Hey, roger that; we'll be right there!"
        )


if __name__ == "__main__":
    s = Sample()
    s.capture()
    rospy.spin()
