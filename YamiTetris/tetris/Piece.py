import random
from variable import Var

#테트리스 블럭 clss
class Piece:
    

    PIECES = {'O': Var.O, 'I': Var.I, 'L': Var.L, 'J': Var.J, 'Z': Var.Z, 'S':Var.S, 'T':Var.T}

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
