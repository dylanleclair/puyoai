import copy
import random
import neuralnetwork

class PuyoEnv:
    w = 6
    h = 13

    def __init__(self, template=None):
        self.board = [[' ' for x in range(self.w)] for y in range(self.h)]
        self.prev_board = [[' ' for x in range(self.w)] for y in range(self.h)]

        # create a neural network for the player
        # first layer = size of input (ie: the size of the board)
        # several internal layers, each with an experimental size
        # finally an output layer, with 4 outputs (one corresponding to each action)

        self.net = neuralnetwork.neural_network([self.w * self.h, 30,30,30, 4])

        # scoring variables
        self.chain = 0 # the current chain length
        self.chain_size = 0 # the number of puyos in the current chain
        self.score = 0 # the players score
        self.diff_colors_in_chain = set() # the size of this will let us determine a bonus
        self.chain_group_sizes = [] # the size of each group in a chain

        self.puyo_to_remove = set()
        self.falling = None
        self.trigger = None
        self.moves = [((-1, 0), (0, 0)),
                      ((-1, 1), (0, 1)),
                      ((-1, 2), (0, 2)),
                      ((-1, 3), (0, 3)),
                      ((-1, 4), (0, 4)),
                      ((-1, 5), (0, 5)),
                      ((0, 0), (-1, 0)),
                      ((0, 1), (-1, 1)),
                      ((0, 2), (-1, 2)),
                      ((0, 3), (-1, 3)),
                      ((0, 4), (-1, 4)),
                      ((0, 5), (-1, 5)),
                      ((-1, 0), (-1, 1)),
                      ((-1, 1), (-1, 2)),
                      ((-1, 2), (-1, 3)),
                      ((-1, 3), (-1, 4)),
                      ((-1, 4), (-1, 5)),
                      ((-1, 1), (-1, 0)),
                      ((-1, 2), (-1, 1)),
                      ((-1, 3), (-1, 2)),
                      ((-1, 4), (-1, 3)),
                      ((-1, 5), (-1, 4))]
        self.buffer = [self.next(), self.next()]
        self.current = self.next()

        row = 0
        col = 0
        if template:
            for puyos in template:
                if puyos == "\n":
                    col += 1
                    row = 0
                    continue
                else:
                    self.board[col][row] = puyos
                    row += 1

    def next(self):
        return random.choice(['1', '2', '3', '4']), random.choice(['1', '2', '3', '4'])

    def scan(self, col, row, chained, color):
        if row < self.w - 1:
            chained = self._check_neighbor(col, row + 1, chained, color)
        if col < self.h - 1:
            chained = self._check_neighbor(col + 1, row, chained, color)
        if row > 0:
            chained = self._check_neighbor(col, row - 1, chained, color)
        if col > 0:
            chained = self._check_neighbor(col - 1, row, chained, color)

        return chained

    def _check_neighbor(self, col, row, chained, color):
        ar_color = self.board[col][row]
        if color == ar_color:
            if (col, row) in chained:
                return chained
            chained.append((col, row))
            chained = self.scan(col, row, chained, color)
        return chained

    def fill(self):
        prev_board = None
        while self.board != prev_board:
            prev_board = copy.deepcopy(self.board)
            for col in range(12, 0, -1):
                for row in range(6):
                    if self.board[col][row] == ' ':
                        self.board[col][row] = self.board[col - 1][row]
                        self.board[col - 1][row] = ' '

    def remove_puyo(self, puyos):
        for x in puyos:
            self.board[x[0]][x[1]] = ' '
        self.puyo_to_remove = set()

    def drop(self):
        self.fill()
        for col in range(self.h):
            for row in range(self.w):
                if (col, row) in self.puyo_to_remove:
                    continue
                color = self.board[col][row]
                chained = [(col, row)]

                if color != ' ':
                    chained = self.scan(col, row, chained, color)

                    # A valid chain is formed
                    if len(chained) >= 4:
                        self.puyo_to_remove = self.puyo_to_remove.union(chained)
                        self.chain_size += len(chained) 
                        self.diff_colors_in_chain.add(color)
                        self.chain_group_sizes.append(len(chained))
    def move(self, display=False):
        self.drop()
        if display:
            self.chain += 1
            if self.chain == 1:
                self.trigger = True
            else:
                self.trigger = False
            self.remove_puyo(self.puyo_to_remove)
            self.drop()
        else:
            while self.puyo_to_remove:
                self.chain += 1
                if self.chain == 1:
                    self.trigger = True
                else:
                    self.trigger = False
                self.remove_puyo(self.puyo_to_remove)
                self.drop()

    # the update function of the puyo board
    def update(self, display=False):
        if self.falling is None:
            self.prev_board = copy.deepcopy(self.board)
            self.move(display=display)
            if self.board == self.prev_board:
                self.update_score() # update the score
                # reset chain specific variables
                self.chain = 0 
                self.chain_size = 0
                self.chain_group_sizes = []
                self.diff_colors_in_chain = set()
                if self.board[1][2] != ' ':
                    print("GAME OVER")
                    return False
                else:
                    colour0, colour1 = self.buffer.pop(0)
                    self.falling = ({'colour': colour0, 'pos': (-1, 2)},
                                    {'colour': colour1, 'pos': (0, 2)})
                    self.buffer.append(self.next())
        else:
            col1, row1 = self.falling[0]['pos']
            col2, row2 = self.falling[1]['pos']

            if (col1 == (self.h - 1) or self.board[col1 + 1][row1] != ' '
                    or col2 == (self.h - 1) or self.board[col2 + 1][row2] != ' '):
                self.board[col1][row1] = self.falling[0]['colour']
                self.board[col2][row2] = self.falling[1]['colour']
                self.falling = None
            else:
                self.falling[0]['pos'] = (col1 + 1, row1)
                self.falling[1]['pos'] = (col2 + 1, row2)

        return True

    def place(self, move):
        pos0, pos1 = self.moves[move]
        col0, col1 = self.current
        self.board[pos0[0] + 1][pos0[1]] = col0
        self.board[pos1[0] + 1][pos1[1]] = col1
        self.drop()

    def play(self, move):
        self.prev_board = copy.deepcopy(self.board)
        self.place(move)
        self.chain = 0
        self.move()
        if self.board[1][2] != ' ':
            print("GAME OVER")
            return False
        else:
            self.current = self.buffer.pop(0)
            self.buffer.append(self.next())
        return True

    def update_score(self):
        # https://puyonexus.com/wiki/Scoring
        self.score += (10 * self.chain_size) * (get_color_bonus(self.diff_colors_in_chain) + get_group_bonus(self.chain_group_sizes))
    def projected_score (self):
        return (10 * self.chain_size) * (get_color_bonus(self.diff_colors_in_chain) + get_group_bonus(self.chain_group_sizes))

    # feeds the board into the neural network
    # gets the output of this, and parses the output into a list
    # indices: 0 = left, 1 = down, 2 = right, 3 = rotate 
    def act(self):

        board_as_floats = []

        for i in range(self.h):
            for j in range(self.w):
                board_as_floats.append(map_board_value_to_float(board[i][j]))
        
        # feed the board to the nn, get 'actions' decided by nn
        actions = net.feed_forward(board_as_floats)

        # round the values to the nearest integer
        return [int(round(x)) for x in actions]

def map_board_value_to_float(v):
    if v == ' ':
        return 0.0
    if v == '1':
        return 1.0
    if v == '2':
        return 2.0
    if v == '3':
        return 3.0


#  https://puyonexus.com/wiki/Scoring#Color_Bonus
'''
Returns the color bonus for a chain
'''
def get_color_bonus(num_colors):
    if  num_colors == 1:
        return 0
    elif num_colors == 2:
        return 3
    elif num_colors ==3:
        return 6
    elif num_colors == 4:
        return 12
    elif num_colors == 5:
        return 24

    return 0

# https://puyonexus.com/wiki/Scoring#Group_Bonus
def get_group_bonus(groups):
    local_sum = 0
    for i in groups:
        if (i <= 10):
            local_sum += i-3
        else: 
            local_sum += 10

    return local_sum

chain_19 = \
    """  3211
122323
323211
123213
232123
321213
232121
232121
211313
123233
312321
312321
312321"""


def main():
    pe = PuyoEnv()
    for x in range(25):
        pe.play(random.randint(0, 21))
        boards = 'Boards:\n'
        for horizontal in zip(pe.board, pe.prev_board):
            boards += ''.join(horizontal[0]) + ' ' + ''.join(horizontal[1]) + '\n'
        print(boards)
        print(f'Chain: {pe.chain}')
        print(f'Puyo Buffer: {pe.buffer}')


if __name__ == '__main__':
    main()
