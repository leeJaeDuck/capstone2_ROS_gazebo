#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity

import rospy; import copy
import math; import time; import numpy as np

from gazebo_msgs.msg    import ModelStates, ModelState
from gazebo_msgs.srv import SetModelState
from std_srvs.srv import Empty
from std_msgs.msg import Float64

pub_score = rospy.Publisher('/score', Float64, queue_size = 10)

firstrun = 0
score = 0.0

 ### first 3 elements : blue balls, last 3 elements : red balls ## 
i_ball = [0,0,0,0,0,0]  ## order of balls
ball_in = [0,0,0,0,0,0] ## 0 : no goal, 1: in line, 2: goal in

model_data = ModelStates()
change = False
ball_cnt = 0
pre_ball_cnt = 0
finish = True

def model_cb(data):
    global model_data, firstrun, change, pre_ball_cnt, score, finish
    if finish == True:
        finish = False
        model_data = data
        if firstrun == 0 :
            memorize_i(data)
            firstrun = 1
        check_score()
        score = sum(ball_in[0:3])*5 + sum(ball_in[3:6])*5


        finish = True


def check_score():
    global ball_in,  ball_cnt

    for i in range(3):
        ball_in[i] = int(dist_goal(i_ball[i])<0.43)

    for i in range(3):
        if goal_in(i_ball[i]) and ball_in[i] ==1:
            ball_in[i] = 2

    for i in range(3):
        ball_in[i+3] = -int(dist_goal(i_ball[i+3])<0.5)
    
    ball_cnt = ball_in.count(1)+ball_in.count(2)

def dist_goal(i):
    dist = math.sqrt(math.pow(8-model_data.pose[i].position.x,2) +math.pow(1.5-model_data.pose[i].position.y,2))
    #print dist
    return dist

def goal_in(i):
    success = model_data.pose[i].position.x>8 
    return success


def change_state():
  #  print "change"
    state_msg = ModelState()
  #  print ball_cnt
    if ball_cnt == 0:
        state_msg.model_name = 'goal_3'
        state_msg.pose.position.x = 5
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0
        send_service(state_msg)
        state_msg.model_name = 'goal_4'
        state_msg.pose.position.x = 5
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0
        send_service(state_msg)
        state_msg.model_name = 'goal_5'
        state_msg.pose.position.x = 5
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0
        send_service(state_msg)
    if ball_cnt == 1:
        state_msg.model_name = 'goal_3'
        state_msg.pose.position.x = 8
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0.6
        send_service(state_msg)
        state_msg.model_name = 'goal_4'
        state_msg.pose.position.x = 5
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0.0
        send_service(state_msg)
        state_msg.model_name = 'goal_5'
        state_msg.pose.position.x = 5
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0.0
        send_service(state_msg)
    if ball_cnt == 2:
        state_msg.model_name = 'goal_3'
        state_msg.pose.position.x = 8
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0.6
        send_service(state_msg)
        state_msg.model_name = 'goal_4'
        state_msg.pose.position.x = 8
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0.8
        send_service(state_msg)
        state_msg.model_name = 'goal_5'
        state_msg.pose.position.x = 5
        state_msg.pose.position.z = 0.0
        send_service(state_msg)
    if ball_cnt == 3:
        state_msg.model_name = 'goal_3'
        state_msg.pose.position.x = 8
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0.6
        send_service(state_msg)
        state_msg.model_name = 'goal_4'
        state_msg.pose.position.x = 8
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 0.8
        send_service(state_msg)
        state_msg.model_name = 'goal_5'
        state_msg.pose.position.x = 8
        state_msg.pose.position.y = 1.5
        state_msg.pose.position.z = 1.0
        send_service(state_msg)



set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
#unpause = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
#pause = rospy.ServiceProxy('/gazebo/pause_physics', Empty)

def send_service(state_msg):

    rospy.wait_for_service('/gazebo/set_model_state')
    try:
        #pause()
        resp = set_state( state_msg )
        #unpause()
       # print "hey"

    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


def memorize_i(data) :
    global i_ball
    for j in range (0,len(data.pose)):
        if data.name[j]=="blue_ball_0" : break
        i_ball[0]=j+1
    for j in range (0,len(data.pose)):
        if data.name[j]=="blue_ball_1" : break
        i_ball[1]=j+1
    for j in range (0,len(data.pose)):
        if data.name[j]=="blue_ball_2" : break
        i_ball[2]=j+1
    for j in range (0,len(data.pose)):
        if data.name[j]=="red_ball_0" : break
        i_ball[3]=j+1
    for j in range (0,len(data.pose)):
        if data.name[j]=="red_ball_1" : break
        i_ball[4]=j+1
    for j in range (0,len(data.pose)):
        if data.name[j]=="red_ball_2" : break
        i_ball[5]=j+1


change_time = 0
def main():
    global change, pre_ball_cnt, change_time
    rospy.init_node('scoring_node', anonymous=True)
    rospy.Subscriber('/gazebo/model_states',ModelStates, model_cb)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        if firstrun != 0 :
            pub_score.publish(score)
            print score
            #print ball_in
            #print(ball_cnt, pre_ball_cnt)

            if ball_cnt != pre_ball_cnt:
                change = True
                change_time = 0
            else:
                change_time = change_time +1
                if change_time >200:
                    change = False
            pre_ball_cnt = ball_cnt

        #if change == True:
        #    change_state()
   
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
