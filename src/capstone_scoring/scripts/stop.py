#!/usr/bin/env python

import rospy; import copy
import math; import time; import numpy as np

from gazebo_msgs.msg    import ModelStates, ModelState
from gazebo_msgs.srv import SetModelState
from std_srvs.srv import Empty
from std_msgs.msg import Float64
from tf.transformations import quaternion_from_euler

case = 1
goal_x = 3.5
goal_y = np.random.uniform(-0.5,0.5)
print(goal_y)
goal_z = 0.5

count = 0

pub_state = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size = 10)

q = quaternion_from_euler(1.570700,0,0)

state_msg = ModelState()
state_msg.model_name = 'stop_sign'
state_msg.pose.position.x = goal_x
state_msg.pose.position.y = goal_y
state_msg.pose.position.z = goal_z
state_msg.pose.orientation.x = q[0]
state_msg.pose.orientation.y = q[1]
state_msg.pose.orientation.z = q[2]
state_msg.pose.orientation.w = q[3]

def main():
    global count, case, current_picture

    rospy.init_node('stop_node', anonymous=True)
    # rospy.spin()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        # set_picture()
        if count < 10:
            print('Stop Sign')
            pub_state.publish(state_msg)
            count = count + 1
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
