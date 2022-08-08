import time
from nuro_arm import RobotArm
from draw_board import *

# robot_move includes all manipulation of the robot

# starting position: side with the control board facing the back

# function for picking up the piece
def pick(robot):
    while True:
        robot.close_gripper()
        gripper_state = robot.get_gripper_state()

        # if something in gripper, drop it off
        if gripper_state > 0.1:
            break
        else: # try again
            robot.open_gripper()
            time.sleep(1)

# function for dropping the piece at the right column
def drop(robot, best_col):
    # jpos1 and jpos2 are motions going towards the board
    jpos1 = [1.1225957748827526, -0.18849555921538758, 0.24294983187761066, 0.6953391739945408, -0.0041887902047863905]
    jpos2 = [0.04607669225265029, -0.18849555921538758, 0.24294983187761066, 0.6953391739945408, -0.0041887902047863905]

    # positions to the corresponding column
    col_pos = [0.5864306286700947, -0.1801179788058148, -0.0041887902047863905, 0.10890854532444616, 0.31834805556376566, 0.460766922526503, 0.6199409503083858]

    pos_place = [col_pos[best_col],0.24713862208239704, 0.20943951023931953, 0.6031857894892403, -0.0041887902047863905]

    # move robot
    robot.move_arm_jpos(jpos1, speed=1.5)
    robot.move_arm_jpos(jpos2, speed=1.5)

    # modify positions for first and last columns
    if best_col == 0:
        pos_place = [-0.343480796792484, 0.5068436147791533, -0.18849555921538758, 0.6576400621514633, 0.012566370614359171]
    elif best_col == 6:
        pos_place = [0.5822418384653083, 0.5696754678509491, -0.24294983187761066, 0.6408849013323178, 0.008377580409572781]

    # move to the right column and drop the piece
    robot.move_arm_jpos(pos_place)
    robot.set_gripper_state(0.4, speed=1.5)

# get robot ready before picking and dropping the piece
def get_ready(robot):
    robot.open_gripper()

    # get into ready-to-pick-up position
    jpos = [1.0681415022205296, -0.2555162024919698, 2.0943951023931953, 0.6408849013323178, -0.04607669225265029]
    robot.move_arm_jpos(jpos)