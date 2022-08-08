# import all functions
from robot_move import *
from camera import *
from draw_board import *

# main_project puts all other parts together

# simulate the game
# note: yellow is robot, which is 2
def main():
    # set up robot
    # connect to robot
    controller_type = 'real'  # real or 'sim'
    robot = RobotArm(controller_type)
    robot.active_mode()

    # create matrix
    board = create_board()

    # if robot's turn, take a pic of board
    take_pic()

    # update matrix
    board = mask(board)

    # find the best column to drop piece
    best_col = find_best_col(board)

    # get robot ready
    get_ready(robot)

    # pick up a piece
    pick(robot)

    # drop piece to best column
    drop(robot, best_col)


    # get back to wait position
    jpos = [0.10053096491487337, -1.3110913340981403, 1.813746158672507, 0.6241297405131722, -0.008377580409572781]
    robot.move_arm_jpos(jpos)

if __name__ == "__main__":
    main()