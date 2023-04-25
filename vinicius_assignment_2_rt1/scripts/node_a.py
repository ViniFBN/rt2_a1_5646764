#! /usr/bin/env python3

"""
A node that implements an action client, allowing the user to set a target :mod:`(x, y)`
or to cancel it. The node also publishes the robot position and velocity :mod:`(x,y, vel_x, vel_z)`
as a custom message :mod:`/node_a_info`, by relying on the values published on the topic :mod:`/odom`. 

Topics
------

Subscribes to:
  * :mod:`/odom`

Publishes to:
  * :mod:`/cmd_vel`
  * :mod:`/node_a_info`
  
Goal actions:
  * :mod:`/reaching_goal_bug`
  * :mod:`/reaching_goal_point`
  * :mod:`/reaching_goal_c`
"""

import rospy
import os
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from vinicius_assignment_2_rt1.msg import node_a_msg
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import *
import time

def clbk_odom(msg):
    """
    Callback function for the :mod:`/odom` topic subscription, reading from the topic message and 
    returning a custom message that contains the position and linear velocity of the 
    robot on :mod:`x` and :mod:`y` directions.

    :param msg: The message received from the publisher containing data for `Pose` and `Twist`.
    :type msg: nav_msgs.msg.Odometry
    """
    global position_, yaw_, pose_

    # position
    position_ = msg.pose.pose.position
    pose_ = msg.pose.pose

    # yaw
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw_ = euler[2]
    
    msg_custom = node_a_msg()
    msg_custom.x = position_.x
    msg_custom.y = position_.y
    msg_custom.vel_x = msg.twist.twist.linear.x
    msg_custom.vel_y = msg.twist.twist.linear.y
    pub.publish(msg_custom)
    
def stp_robot():
    """
    Function that publishes a message of type *Twist* with values equal to 0,
    in order to stop the robot, to the topic :mod:`/cmd_vel`.
    """
    twist_msg.linear.x = 0
    twist_msg.angular.z = 0
    pub_twist.publish(twist_msg)

def main():
    """
    Main function of the node. Initializes the node and sets up publishers and subscribers, 
    as well as communication with action servers while waiting for new goals to be set. 
    
    Checks if the *cancel* command is active, in order to cancel the goal set by the user,
    also checking the new goal parameteres sent to the program.
    """
    global pub, pub_twist, twist_msg
    
    rospy.on_shutdown(stp_robot) # Capturing the stop part
    rospy.init_node('node_a')
    
        
    # Custom message part
    twist_msg = Twist()
    pub_twist = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
    pub = rospy.Publisher('/node_a_info', node_a_msg, queue_size=1)
    can_var = rospy.get_param(rospy.search_param("cancel"))
    if can_var == True:
        print("Cancelling current target goal.\n")
        rospy.set_param(rospy.search_param("cancel"), False)
        stp_robot()
        os.system("rosnode kill /node_a")
        sys.exit(0)
    
    ## Action client part
    # to bug_as.py
    act_c_bug = actionlib.SimpleActionClient('/reaching_goal_bug', assignment_2_2022.msg.PlanningAction)
    act_c_bug.wait_for_server() # Waiting for the action server
    # to go_to_point_service.py
    act_c_point = actionlib.SimpleActionClient('/reaching_goal_point', assignment_2_2022.msg.PlanningAction)
    act_c_point.wait_for_server() # Waiting for the action server
    # to node_c.py
    act_c_c = actionlib.SimpleActionClient('/reaching_goal_c', assignment_2_2022.msg.PlanningAction)
    act_c_c.wait_for_server() # Waiting for the action server
    
    
    # Goal to be sent to the action server
    goal_send = assignment_2_2022.msg.PlanningGoal() 
    
    # Target location
    goal_send.target_pose.pose.position.x = rospy.get_param(rospy.search_param('x'))
    goal_send.target_pose.pose.position.y = rospy.get_param(rospy.search_param('y'))
    
    # Sending the goal to the server
    act_c_bug.send_goal(goal_send)
    act_c_point.send_goal(goal_send)
    act_c_c.send_goal(goal_send)
    
    rospy.delete_param(rospy.search_param('x'))
    rospy.delete_param(rospy.search_param('y'))
    
    # Blocking signals until goal is reached
    act_c_bug.wait_for_result() # Waits for the server to finish the action sent
    act_c_bug.get_result() # Gets result from the server (PlanningResult)
    
    act_c_point.wait_for_result() # Waits for the server to finish the action sent
    act_c_point.get_result() # Gets result from the server (PlanningResult)
    
    act_c_c.wait_for_result() # Waits for the server to finish the action sent
    act_c_c.get_result() # Gets result from the server (PlanningResult)

if __name__ == "__main__":
    main()
