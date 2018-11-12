import copy
import sys
import time
new_move = (-1, -1)

class Team38:
    def __init__(self):
        self.max_depth = 1
        self.count_p = 0
        self.count_o = 0
        self.start = 0
        self.utility = 0
        self.num = 0
        self.patterns = [
            # diamonds
            ((1, 2), (2, 1), (2, 3), (3, 2)),
            ((1, 1), (2, 0), (2, 2), (3, 1)),
            ((0, 2), (1, 1), (1, 3), (2, 2)),
            ((0, 1), (1, 0), (1, 2), (2, 1)),
            # rows
            ((0, 0), (0, 1), (0, 2), (0, 3)),
            ((1, 0), (1, 1), (1, 2), (1, 3)),
            ((2, 0), (2, 1), (2, 2), (2, 3)),
            ((3, 0), (3, 1), (3, 2), (3, 3)),
            # columns
            ((0, 0), (1, 0), (2, 0), (3, 0)),
            ((0, 1), (1, 1), (2, 1), (3, 1)),
            ((0, 2), (1, 2), (2, 2), (3, 2)),
            ((0, 3), (1, 3), (2, 3), (3, 3))
        ]

    def get_allowed_cells(self, board, block, old_move):
        allowed_cells = []
        row = old_move[0] % 4
        column = old_move[1] % 4

        if old_move != (-1, -1) and block[row][column] == '-':
			for i in range(4 * row, 4 * row + 4):
				for j in range(4 * column, 4 * column + 4):
					if board[i][j] == '-':
						allowed_cells.append((i, j))
        else:
			for i in range(16):
				for j in range(16):
					if block[i/4][j/4] == '-' and board[i][j] == '-':
						allowed_cells.append((i, j))
        return allowed_cells

    def get_utility(self, board, block, flag, opp_flag, old_move):
        util = 0

        net_blocks = 0
        corner_blocks = 0
        mid_blocks = 0
        side_blocks = 0

        for i in range(0, 4):
            for j in range(0, 4):
                if (i == 0 or i == 3) and (j == 0 or j == 3):
                    if block[i][j] == flag:
                        corner_blocks += 1
                    elif block[i][j] == opp_flag:
                        corner_blocks -= 1
                elif (i == 1 or i == 2) and (j == 1 or j == 2):
                    if block[i][j] == flag:
                        mid_blocks += 1
                    elif block[i][j] == opp_flag:
                        mid_blocks -= 1
                else:
                    if block[i][j] == flag:
                        side_blocks += 1
                    elif block[i][j] == opp_flag:
                        side_blocks -= 1

        net_blocks = corner_blocks + mid_blocks + side_blocks
        util += (net_blocks * 4 * 10)
        '''util += (corner_blocks * 6 * 10)
        util += (mid_blocks * 3 * 10)
        util += (side_blocks * 4 * 10)'''

        for i in self.patterns:
            count_o = 0
            count_p = 0
            for j in i:
                if block[j[0]][j[1]] == flag:
                    count_p += 1
                elif block[j[0]][j[1]] == opp_flag:
                    count_o += 1
            #util += ((count_p * 1250) - (count_o * 1250))
            if count_p != 0:
                count_p -= 1
                util += ((10**count_p))
            if count_o != 0:
                count_o -= 1
                util -= ((10**count_o) + (100 * count_o))


        block_x = old_move[0] % 4
        block_y = old_move[1] % 4
        if block[block_x][block_y] != '-': # ?????????????? oldmove[0]/4
            util -= 500


        for p in range(0, 4):
            for q in range(0, 4):
                a = 4 * p
                b = 4 * q
                for i in self.patterns:
                    count_o = 0
                    count_p = 0
                    for j in i:
                        if board[a + j[0]][b + j[1]] == flag:
                            count_p += 1
                        elif board[a + j[0]][b + j[1]] == opp_flag:
                            count_o += 1
                    #util += ((count_p * 1250) - (count_o * 1250))
                    if count_p != 0:
                        count_p -= 1
                        util += (10**count_p)
                    if count_o != 0:
                        count_o -= 1
                        util -= ((10**count_o) + (100 * count_o))

        #current block
        block_x = old_move[0] / 4
        block_y = old_move[1] / 4
        block_x *= 4
        block_y *= 4
        for i in self.patterns:
            count_o = 0
            count_p = 0
            for j in i:
                if board[block_x + j[0]][block_y + j[1]] == flag:
                    count_p += 1
                elif board[block_x + j[0]][block_y + j[1]] == opp_flag:
                    count_o += 1
            #util += ((count_p * 1250) - (count_o * 1250))
            if count_p != 0:
                count_p -= 1
                util += (10**count_p)
            if count_o != 0:
                count_o -= 1
                util -= ((10**count_o) + (100 * count_o))

        return util


    def alphabeta(self, board, block, old_move, depth, flag, opp_flag, alpha, beta, maxnode, row, column):
        if depth == self.max_depth:
            self.utility = self.get_utility(board, block, flag, opp_flag, old_move)
            return (row, column, self.utility)

        else:
            cells = self.get_allowed_cells(board, block, old_move)
            if len(cells) == 0:
                self.utility = self.get_utility(board, block, flag, opp_flag, old_move)
                return (old_move[0], old_move[1], self.utility)

            for cell in cells:
                temp_flag = 0
                if maxnode:
                    board[cell[0]][cell[1]] = flag
                else:
                    board[cell[0]][cell[1]] = opp_flag

                block_x = cell[0] / 4
                block_y = cell[1] / 4
                k = 0
                for i in self.patterns:
                    lx = 0
                    ly = 0
                    for j in i:
                        if board[block_x*4 + j[0]][block_y*4 + j[1]] == 'x':
                            lx += 1
                        elif board[block_x*4 + j[0]][block_y*4 + j[1]] == 'o':
                            ly += 1

                    if lx == 4:
                        temp_flag = 1
                        block[block_x][block_y] = 'x'
                        break
                    elif ly == 4:
                        temp_flag = 1
                        block[block_x][block_y] = 'o'
                        break

                for i in range(0, 4):
                    for j in range(0, 4):
                        if block[i][j] != '-':
                            k += 1
                if k == 16 and temp_flag == 0:
                    temp_flag = 1
                    block[block_x][block_y] = 'd'

                if maxnode:
                    self.utility = self.alphabeta(board, block, cell, depth + 1, flag, opp_flag, alpha, beta, False, row, column)[2]
                    if self.utility > alpha:
                        alpha = self.utility
                        row = cell[0]
                        column = cell[1]
                    #if time.clock() - self.start > 14.5:
                    #    return (row, column, alpha)
                else:
                    self.utility = self.alphabeta(board, block, cell, depth + 1, flag, opp_flag, alpha, beta, True, row, column)[2]
                    if self.utility < beta:
                        beta = self.utility
                        row = cell[0]
                        column = cell[1]
                    #if time.clock() - self.start > 14.5:
                    #    return (row, column, beta)

                board[cell[0]][cell[1]] = '-'
                if temp_flag:
                    block[block_x][block_y] = '-'

                if alpha >= beta:
                    break

            if depth == 0:
                if row == '-1' or column == '-1':
                    row = cells[0][0]
                    column = cells[0][1]

            if maxnode:
                return (row, column, alpha)
            else:
                return (row, column, beta)


    def move(self, board, old_move, flag):
        global new_move
        self.start = time.clock()
        self.max_depth = 4
        self.utility = 0
        self.num += 1

        if flag == 'x':
            opp_flag = 'o'
        else:
            opp_flag = 'x'

        if old_move == (-1, -1):
            return (1, 5)

        depth = 5
        if self.num > 120:
            self.max_depth = depth

        temp_board = copy.deepcopy(board.board_status) # status of 16 x 16
        temp_block = copy.deepcopy(board.block_status) # status of 4 X 4

        new_move = self.alphabeta(temp_board, temp_block, old_move, 0, flag, opp_flag, -100000000, 100000000, True, -1, -1)

        #time_taken = (time.clock() - self.start)
        #print time_taken

        return (new_move[0], new_move[1])
