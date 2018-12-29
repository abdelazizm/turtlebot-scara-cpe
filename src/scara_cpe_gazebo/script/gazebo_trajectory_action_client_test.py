#!/usr/bin/env python
import roslib
roslib.load_manifest('scara_cpe_gazebo')

import rospy
import actionlib
from std_msgs.msg import Float64
import trajectory_msgs.msg
import control_msgs.msg
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import JointTrajectoryAction, JointTrajectoryGoal, FollowJointTrajectoryAction, FollowJointTrajectoryGoal

from pynput.keyboard import Key, Listener




class Joint:
        def __init__(self):
            self.x=0
            self.y=0
            self.jta = actionlib.SimpleActionClient('/scara_cpe/scara_cpe_controller/follow_joint_trajectory', FollowJointTrajectoryAction)
            rospy.loginfo('Waiting for joint trajectory action')
            self.jta.wait_for_server()
            rospy.loginfo('Found joint trajectory action!')
            with Listener(on_press=self.on_press) as listener:
                listener.join()

        def move_joint(self, angles):
            goal = FollowJointTrajectoryGoal()
            goal.trajectory.joint_names = ['shoulder_1_joint', 'shoulder_2_joint']
            point = JointTrajectoryPoint()
            point.positions = angles
            point.time_from_start = rospy.Duration(3)
            goal.trajectory.points.append(point)
            self.jta.send_goal_and_wait(goal)

        def on_press(self,key):
            print('{0} pressed'.format(
                key))
            if key== Key.right:
                self.x=self.x-0.5
                self.y=self.y-0.5
            if key== Key.left:
                self.x=self.x+0.5
                self.y=self.y+0.5
            if key == Key.esc:
                # Stop listener
                return False
            print(self.x, self.y)
            self.move_joint([self.x,self.y])




def main():
    arm = Joint()



if __name__ == '__main__':
      rospy.init_node('joint_position_tester')
      main()
