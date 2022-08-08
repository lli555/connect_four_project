import numpy as np
import cv2
import math
import statistics
from statistics import mode

# draw_board includes all manipulation about a virtual copy of the board

# create the board with matrix
def create_board():
    board = np.zeros((6, 7))
    return board


# masked image for red, yellow, and blue
def mask(board):
    # when called, fill in either red or yellow pieces depending on input code
    def re_fill(cell_width, cell_height, mask, board, code):
        # iterate over each cell to look for white pixels
        for x in range(7):
            for y in range(6):
                for i in range(cell_width):
                    for j in range(cell_height):
                        color = mask[y * cell_height + j, x * cell_width + i]
                        # if detected a white pixel, fill its corresponding cell
                        if color == 255 and code == 'red':
                            board[y, x] = 1
                        elif color == 255 and code == 'yellow':
                            board[y, x] = 2
        return board

    # read in image
    img = cv2.imread("Cropped Image.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # yellow mask
    # note: increase low's v value for more accuracy
    # yellow_low = np.array([15, 100, 120])
    yellow_low = np.array([15, 100, 150])
    yellow_up = np.array([36, 255, 255])
    mask = cv2.inRange(img, yellow_low, yellow_up)

    # red mask
    # red_low = np.array([0, 100, 120])
    red_low = np.array([0, 100, 150])
    red_up = np.array([10, 255, 255])
    mask2 = cv2.inRange(img, red_low, red_up)

    # blue
    # blue_low = np.array([90, 100, 120])
    # blue_up = np.array([140, 255, 255])
    # mask3 = cv2.inRange(img, blue_low, blue_up)

    # cv2.imshow('mask', mask2)

    # store parameters for re_fill function
    width = img.shape[1]
    height = img.shape[0]
    cell_width = math.floor(width / 7)
    cell_height = math.floor(height / 6)

    board = re_fill(cell_width, cell_height, mask, board, 'yellow')  # fill in yellow pieces
    board = re_fill(cell_width, cell_height, mask2, board, 'red')  # fill in red pieces

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return board


# check if there is a winner yet
def check_winner(board):
    # check if there is a winner by making a four
    rows = len(board)
    cols = len(board[0])
    winner = 0

    count = []

    # horizontal check
    for i in range(rows):  # 6 times
        for j in range(cols - 3):  # 4 times
            count.clear()
            for x in range(4):
                if board[i, j + x] != 0:
                    count.append(board[i, j + x])
            if len(count) == 4 and len(set(count)) == 1:
                winner = count[0]

    # vertical check
    for i in range(cols):  # 7 times
        for j in range(rows - 3):  # 3 times
            count.clear()
            for x in range(4):
                if board[j + x, i] != 0:
                    count.append(board[j + x, i])
            if len(count) == 4 and len(set(count)) == 1:
                winner = count[0]

    # check diagonal top left -> SE
    for i in range(rows - 3):  # 3 times
        for j in range(cols - 3):  # 4 times
            count.clear()
            for x in range(4):
                if board[x + i, x + j] != 0:
                    count.append(board[x + i, x + j])
            if len(count) == 4 and len(set(count)) == 1:
                winner = count[0]

    # check diagonal top right -> SW
    b = 6
    for a in range(rows - 3):
        b = 6
        while b > cols - 5:
            count.clear()
            for x in range(4):
                if board[a + x, b - x] != 0:
                    count.append(board[a + x, b - x])
            if len(count) == 4 and len(set(count)) == 1:
                winner = count[0]

            b -= 1

    # return the status of winner
    if winner != 0:
        return winner
    else:  # else there isn't a winner
        # check if there is a tie by checking if top row is full
        for i in range(7):
            if board[0, i] == 0:
                return None   # if not full and no winner

        return 'tie'

# find a random column to place piece
def find_random_col(board):
    # check if first row of column is occupied
    nonfull_columns = [i for i in range(7) if board[0, i] == 0]
    print('nonfull col', nonfull_columns)
    col_to_place = np.random.choice(nonfull_columns)
    print('col selected', col_to_place)
    empty_row = np.where(board[:, col_to_place] == 0)[0][-1]
    print('empty row', empty_row)
    board[empty_row, col_to_place] = 2
    print(board)

    return col_to_place

# give an estimated score for board state after all depths
def guess_score(board):
    # intialization
    rows = 6
    cols = 7
    score = 0
    count = []

    # horizontal check
    for i in range(rows):  # 6 times
        for j in range(cols - 3):  # 4 times
            count.clear()
            for x in range(4):
                if board[i, j + x] != 0:
                    count.append(board[i, j + x])
            if len(count) == 4 and len(set(count)) == 1:
                if mode(count) == 1.0:
                    score -= 1
                elif mode(count) == 2.0:
                    score += 1

    # vertical check
    for i in range(cols):  # 7 times
        for j in range(rows - 3):  # 3 times
            count.clear()
            for x in range(4):
                if board[j + x, i] != 0:
                    count.append(board[j + x, i])
            if len(count) == 4 and len(set(count)) == 1:
                if mode(count) == 1.0:
                    score -= 1
                elif mode(count) == 2.0:
                    score += 1

    # check diagonal top left -> SE
    for i in range(rows - 3):  # 3 times
        for j in range(cols - 3):  # 4 times
            count.clear()
            for x in range(4):
                if board[x + i, x + j] != 0:
                    count.append(board[x + i, x + j])
            if len(count) == 4 and len(set(count)) == 1:
                if mode(count) == 1.0:
                    score -= 1
                elif mode(count) == 2.0:
                    score += 1

    # check diagonal top right -> SW
    b = 6
    for a in range(rows - 3):
        b = 6
        while b > cols - 5:
            count.clear()
            for x in range(4):
                if board[a + x, b - x] != 0:
                    count.append(board[a + x, b - x])
            if len(count) == 4 and len(set(count)) == 1:
                if mode(count) == 1.0:
                    score -= 1
                elif mode(count) == 2.0:
                    score += 1
            b -= 1

    return score

# find the column with the highest probability towards middle column
def random_col(index_list):
    prob_list = np.array([1, 5, 30, 100, 30, 5, 1])
    prob = prob_list[np.array(index_list)]
    prob = prob/prob.sum()
    # prob = []
    #
    # for i in range(prob_list):
    #     prob_list[i] = prob_list[i]/sum(prob_list)
    #
    #
    #
    # for each in index_list:
    #     prob.append(prob_list[each])

    rand_col = np.random.choice(index_list, p=prob)

    return rand_col

# function for finding the most ideal column to place piece
def find_best_col(board):
    # create a dictionary
    scores = {2.0: 100, 1.0: -100, 'tie': 0}

    # define minimax
    def minimax(board, depth, isMax):
        # first check if someone won; winner, 'tie', None
        result = check_winner(board)
        # print(result)

        # if the game is over return score
        if result != None:
            score = scores[result]

            return score

        # if reach an end, give an estimated score for current state
        if depth == 0:
            score = guess_score(board)

            return score

        # if is maximizer, check all spots to find best possible outcome and return it
        if isMax is True:
            bestscore = -math.inf
            # check all spots in lowest row that are available
            nonfull_columns = [i for i in range(7) if board[0, i] == 0]
            for each in nonfull_columns:
                empty_row = np.where(board[:, each] == 0)[0][-1]

                # place 2 on spot available
                board[empty_row, each] = 2
                # call minimax again
                score = minimax(board.copy(), depth - 1, False)
                # set spot to 0 again to undo move
                board[empty_row, each] = 0

                bestscore = max(score, bestscore) # update bestscore

            return bestscore
        # minimizer's turn
        else:
            bestscore = math.inf

            # check all spots in lowest row that are available
            nonfull_columns = [i for i in range(7) if board[0, i] == 0]
            for each in nonfull_columns:
                empty_row = np.where(board[:, each] == 0)[0][-1]

                # place 1 on spot available
                board[empty_row, each] = 1
                # call minimax again
                score = minimax(board.copy(), depth - 1, True)
                # set spot to 0 again to undo move
                board[empty_row, each] = 0

                bestscore = min(score, bestscore)  # update bestscore

            return bestscore

    # declare
    bestscore = -math.inf
    bestcol = 0
    all_scores = []

    # check all spots in lowest row that are available
    nonfull_columns = [i for i in range(7) if board[0, i] == 0]
    for each in nonfull_columns:
        empty_row = np.where(board[:, each] == 0)[0][-1]

        # place 2 on spot available
        board[empty_row, each] = 2
        # print(board)
        # call minimax again
        score = minimax(board.copy(), 4, False)

        # add score for each non-empty col into a list
        all_scores.append(score)

        # set spot to 0 again to undo move
        board[empty_row, each] = 0

        # print(each, score)

    # find the best col towards middle
    max_score = max(all_scores)
    print(nonfull_columns)
    index_list = [nonfull_columns[index] for index in range(len(all_scores)) if all_scores[index] == max_score]
    bestcol = random_col(index_list)
    print(all_scores)
    print(bestcol)

    return bestcol
