#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity

import rospy; import copy
import math; import time; import numpy as np

from gazebo_msgs.msg    import ModelStates, ModelState
from gazebo_msgs.srv import SetModelState
from std_srvs.srv import Empty
from std_msgs.msg import Float64
from tf.transformations import quaternion_from_euler

case = 1
goal_x = -3.8
goal_y = 0
goal_z = 1.3

count = 0

pub_state = rospy.Publisher('/gazebo/set_model_state', ModelState, queue_size = 10)

def case_permutation(i):
    global picture1, picture2, picture3, current_picture
    # dog picture : 1
    # cat picture : 2
    if i == 1:
        picture1 = 1 
        picture2 = 1
        picture3 = 2
    elif i == 2:
        picture1 = 1
        picture2 = 2
        picture3 = 1
    elif i == 3:
        picture1 = 2
        picture2 = 1
        picture3 = 1
    current_picture = picture1


front_q = quaternion_from_euler(1.570700,0,1.570700)
back_q = quaternion_from_euler(1.570700,0,-1.570700)

dog_state_msg = ModelState()
dog_state_msg.model_name = 'dog'
dog_state_msg.pose.position.x = goal_x
dog_state_msg.pose.position.y = goal_y
dog_state_msg.pose.position.z = goal_z
dog_state_msg.pose.orientation.x = front_q[0]
dog_state_msg.pose.orientation.y = front_q[1]
dog_state_msg.pose.orientation.z = front_q[2]
dog_state_msg.pose.orientation.w = front_q[3]

cat_state_msg = ModelState()
cat_state_msg.model_name = 'cat'
cat_state_msg.pose.position.x = goal_x
cat_state_msg.pose.position.y = goal_y
cat_state_msg.pose.position.z = goal_z
cat_state_msg.pose.orientation.x = back_q[0]
cat_state_msg.pose.orientation.y = back_q[1]
cat_state_msg.pose.orientation.z = back_q[2]
cat_state_msg.pose.orientation.w = back_q[3]

def set_picture():
    global current_picture, front_q, back_q, dog_state_msg, cat_state_msg

    if current_picture == 1 : # show dog picture
        dog_state_msg.pose.orientation.x = front_q[0]
        dog_state_msg.pose.orientation.y = front_q[1]
        dog_state_msg.pose.orientation.z = front_q[2]
        dog_state_msg.pose.orientation.w = front_q[3]
        cat_state_msg.pose.orientation.x = back_q[0]
        cat_state_msg.pose.orientation.y = back_q[1]
        cat_state_msg.pose.orientation.z = back_q[2]
        cat_state_msg.pose.orientation.w = back_q[3]
        
    else: 
        dog_state_msg.pose.orientation.x = back_q[0]
        dog_state_msg.pose.orientation.y = back_q[1]
        dog_state_msg.pose.orientation.z = back_q[2]
        dog_state_msg.pose.orientation.w = back_q[3]
        cat_state_msg.pose.orientation.x = front_q[0]
        cat_state_msg.pose.orientation.y = front_q[1]
        cat_state_msg.pose.orientation.z = front_q[2]
        cat_state_msg.pose.orientation.w = front_q[3]  
    
    pub_state.publish(dog_state_msg)
    pub_state.publish(cat_state_msg)


def current_ball_cb(data):
    global picture1, picture2, picture3, current_picture, count
    print('Finished %d ball' %data.data)
    if data.data == 1.0 : # completed first ball
        current_picture = picture2

    elif data.data == 2.0 : # completed second ball
        current_picture = picture3

    if current_picture == 1 :
        print('dog')
    elif current_picture == 2 :
        print('cat')
    # set_picture()
    count = 0

def main():
    global count, case, current_picture
    case_permutation(case)

    rospy.init_node('animal_topic_node', anonymous=True)
    rospy.Subscriber('/current_ball',Float64, current_ball_cb)
    # rospy.spin()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        # set_picture()
        if count < 5:
            print('Picture Reset')
            set_picture()
            count = count + 1
        rate.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
