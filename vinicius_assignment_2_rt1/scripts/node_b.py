#! /usr/bin/env python3
    
""" aaa

_extended_summary_

"""

import rospy
import actionlib
import actionlib.msg
from vinicius_assignment_2_rt1.srv import node_b_srv, node_b_srvResponse, node_b_srvRequest
from geometry_msgs.msg import Point, Pose, Twist
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import *

i_goal = 0
i_cancel = 0

def clbk_srv(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    global req_var_stat
    global i_goal, i_cancel # Variable to count the number of responses obtained
    
    req_var_stat = request.stat
    
    response = node_b_srvResponse()
    if req_var_stat == True:
        i_goal = i_goal + 1
        response.goal_num = i_goal
        print("Number of goals reached:",response.goal_num)
    elif req_var_stat == False:
        i_cancel = i_cancel + 1
        response.cancel_num = i_cancel
        print("Number of goals cancelled:",response.cancel_num)
    return response    
    

def main():
    global serv
    rospy.init_node('node_b')
    print("===== Node B - Service to show how many goals were reached/cancelled =====\n")
    serv = rospy.Service('node_b_service', node_b_srv, clbk_srv)
    rospy.spin()
    
    
if __name__ == "__main__":
    main()
