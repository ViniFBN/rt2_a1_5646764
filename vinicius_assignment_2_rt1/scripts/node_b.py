#! /usr/bin/env python3
    
""" 
A service node that, when called, prints the number of goals reached and/or cancelled.

Topics
------

Services:
  * :mod:`node_b_service`
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
    """
    Callback function for the service :mod:`node_b_service`, which is responsible 
    for updating and returning the statistics of goals reached and cancelled based 
    on the input :mod:`request` object. Returns a feedback :mod:`response`.
    
    :param request: The request object containing the :mod:`stat` attribute.
    :type request: node_b_srvRequest
    :return: A :mod:`node_b_srvResponse` object with the updated goal and/or cancel count.
    :rtype: node_b_srvResponse
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
    """
    Main function of the node. Initializes the node and sets up the service to print information
    on the console whenever a goal is achieved/cancelled.
    """
    global serv
    rospy.init_node('node_b')
    print("===== Node B - Service to show how many goals were reached/cancelled =====\n")
    serv = rospy.Service('node_b_service', node_b_srv, clbk_srv)
    rospy.spin()
    
    
if __name__ == "__main__":
    main()
