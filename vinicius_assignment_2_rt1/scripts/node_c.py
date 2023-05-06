#! /usr/bin/env python3

"""
A node that subscribes to the robot's position and velocity (using the custom message from :mod:`/node_a_info`)
and prints the distance of the robot from the target and the robot's average speed.

The node uses a parameter :mod:`des_rate_c` to set how fast it publishes the information.

Topics
------

Subscribes to:
  * :mod:`/node_a_info`
  
Goal actions:
  * :mod:`/reaching_goal_c`
"""

import rospy
import math
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from vinicius_assignment_2_rt1.msg import node_a_msg
from geometry_msgs.msg import Point, Pose, Twist
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import *
import time

# global variables
vel_list_x = []
vel_list_y = []

pos_print_x = 0
pos_print_y = 0
vel_print_x = 0
vel_print_y = 0

desired_position_ = Point()
desired_position_.z = 0

def clbk_function(msg):
    """
    Callback function for the :mod:`/node_a_info` topic subscription, reading the published
    information on position and velocity and calculating the distance to goal and
    average velocity, on both directions :mod:`x` and :mod:`y`.
    
    :param msg: The message received from the publisher containing data for `Pose` and `Twist`.
    :type msg: vinicius_assignment_2_rt1.msg.node_a_msg
    """
    global pos_print_x, pos_print_y, vel_print_x, vel_print_y
    
    # Position
    pos_current_x = msg.x
    pos_current_y = msg.y
    
    posx = desired_position_.x
    posy = desired_position_.y
    pos_print_x = pos_current_x - posx
    pos_print_y = pos_current_y - posy
    
    # Average velocity
    vel_current_x = msg.vel_x
    vel_current_y = msg.vel_y
    
    # CALCULATE AVERAGE VELOCITY HERE
    vel_list_x.append(vel_current_x)
    vel_list_y.append(vel_current_y)
    
    vel_print_x = sum(vel_list_x)/len(vel_list_x)
    vel_print_y = sum(vel_list_y)/len(vel_list_y)
    
def desired_pos(goal):
    """
    Function used on the simple action server :mod:`/reaching_goal_c`. Sets the
    desired position of the goal.
    
    :param goal: The request object containing the :mod:`target_pose` attribute.
    :type goal: assignment_2_2022.msg.PlanningAction
    """
    global act_s
    desired_position_.x = goal.target_pose.pose.position.x
    desired_position_.y = goal.target_pose.pose.position.y
    
    feedback = assignment_2_2022.msg.PlanningFeedback()
    result = assignment_2_2022.msg.PlanningResult()
    
    feedback.stat = "Goal defined."
    act_s.set_succeeded(result)
    
def main():
    """
    Main function of the node. Initializes the node and sets up the action server, as well as
    subscribing to :mod:`/node_a_info` topic. Sets up the frequency in which the information
    is posted on the console.
    """
    global act_s
    rospy.init_node('node_c')
    
    # Starting the action server
    act_s = actionlib.SimpleActionServer('/reaching_goal_c', assignment_2_2022.msg.PlanningAction, desired_pos, auto_start=False)
    act_s.start()
    
    sub_custom = rospy.Subscriber('/node_a_info', node_a_msg, clbk_function)
    
    rate_c = rospy.get_param('des_rate_c')
    rate = rospy.Rate(rate_c)
    while not rospy.is_shutdown():
        print("\nDistance to the goal: \nx:", pos_print_x,"\ny:", pos_print_y,"\nNorm:",math.sqrt(pow(pos_print_x, 2) + pow(pos_print_y, 2)))
        print("\nAverage velocity of the robot: \nvel_x:", vel_print_x,"\nvel_y:", vel_print_y)
        print("\n=====================================================")
        
        rate.sleep()
    
if __name__ == "__main__":
    main()