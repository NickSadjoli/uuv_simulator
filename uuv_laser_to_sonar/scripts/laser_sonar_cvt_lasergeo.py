#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud, PointCloud2, LaserScan
import laser_geometry.laser_geometry as lg 
import math
import numpy as np


#initialize node
rospy.init_node("uuv_sonar_to_pointcloud")

#initialize laser projection object
laser_project = lg.LaserProjection()

#converts laser data to sonar image
def laser_sonar_cvt(laser_msg):

    #convert laser_msgs into pc2 type messages first
    pc2_msg = laser_project.projectLaser(laser_msg)



pc_pub = rospy.Publisher("sonar_scan_pointcloud", PointCloud2, queue_size=1)

def scan_cb(msg):
    # convert the message of type LaserScan to a PointCloud2
    pc2_msg = laser_project.projectLaser(msg)

    # now we can do something with the PointCloud2 for example:
    # publish it
    pc_pub.publish(pc2_msg)
    
    # convert it to a generator of the individual points
    point_generator = pc2.read_points(pc2_msg)
    

    # we can access a generator in a loop
    sum = 0.0
    num = 0
    for point in point_generator:
        if not math.isnan(point[2]):
            sum += point[2]
            num += 1
    # we can calculate the average z value for example
    print("average z value", str(sum/num), str(num), point_generator)

    # or a list of the individual points which is less efficient
    point_list = pc2.read_points_list(pc2_msg)

    # we can access the point list with an index, each element is a namedtuple
    # we can access the elements by name, the generator does not yield namedtuples!
    # if we convert it to a list and back this possibility is lost
    print("point list tuples", len(point_list), point_list[200], point_list[len(point_list)/2].x)


rospy.Subscriber("rexrov/sonar", LaserScan, scan_cb, queue_size=1)
rospy.spin()



