import random
from variable import Var

# Tetrimino colors
#cyan = (69, 206, 204) #rgb(69, 206, 204) # I
#blue = (64, 111, 249) #rgb(64, 111, 249) # J
#orange = (253, 189, 53) #rgb(253, 189, 53) # L
#yellow = (246, 227, 90) #rgb(246, 227, 90) # O
#green = (98, 190, 68) #rgb(98, 190, 68) # S
#pink = (242, 64, 235) #rgb(242, 64, 235) # T
#red = (225, 13, 27) #rgb(225, 13, 27) # Z

#테트리스 블럭 clss
class Piece:
    

    PIECES = {'O': Var.O, 'I': Var.I, 'L': Var.L, 'J': Var.J, 'Z': Var.Z, 'S':Var.S, 'T':Var.T}

    #T_COLOR = [yellow ,cyan, orange, blue, red, green, pink, (55, 55, 55)]



    def __init__(self, piece_name=None):
        if piece_name:
            self.piece_name = piece_name
        else:
            self.piece_name = random.choice(list(Piece.PIECES.keys()))
        self.rotation = Var.initial_block_state
        self.array2d = Piece.PIECES[self.piece_name][self.rotation]

    def __iter__(self):
        for row in self.array2d:
            yield row

    def rotate(self, clockwise=True):
        if clockwise:
            self.rotation = (self.rotation + Var.next_block_shape) % Var.rotate_cycle
        else:
            self.rotation = (self.rotation  - Var.next_block_shape) % Var.rotate_cycle
        self.array2d = Piece.PIECES[self.piece_name][self.rotation]
