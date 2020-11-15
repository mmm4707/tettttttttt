from ai_field import ai_Field
import copy

def ai_rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]


class Ai:

    @staticmethod
    def best(ai_field, workingPieces, workingPieceIndex, weights, ai_level):
        bestRotation = None
        bestOffset = None
        bestScore = -10000
        workingPieceIndex = copy.deepcopy(workingPieceIndex)
        workingPiece = workingPieces[workingPieceIndex]
        shapes_rotation = { 4 : 4, 8 : 2, 12 : 2, 16 : 4, 20 : 4, 24 : 2, 28 : 1 }
        flat_piece = [val for sublist in workingPiece for val in sublist]
        hashedPiece = sum(flat_piece)

        for rotation in range(0, shapes_rotation[hashedPiece]):
            for offset in range(0, ai_field.ai_width):
                result = ai_field.projectPieceDown(workingPiece, offset, ai_level)
                if not result is None:
                    score = None
                    if workingPieceIndex == len(workingPieces)-1 :
                        heuristics = ai_field.heuristics()
                        score = sum([a*b for a,b in zip(heuristics, weights)])
                    else:
                        _, _, score = Ai.best(ai_field, workingPieces, workingPieceIndex + 1, weights, 2)

                    if score > bestScore :
                        bestScore = score
                        bestOffset = offset
                        bestRotation = rotation
                ai_field.undo(ai_level)
            workingPiece = ai_rotate_clockwise(workingPiece)

        return bestOffset, bestRotation, bestScore

    @staticmethod
    def choose(initialField, piece, next_piece, offsetX, weights, parent):
        ai_field = ai_Field(len(initialField[0]), len(initialField))
        ai_field.updateField(copy.deepcopy(initialField))

        offset, rotation, _ = Ai.best(ai_field, [piece, next_piece], 0, weights, 1)
        moves = []

        offset = offset - offsetX
        for _ in range(0, rotation):
            moves.append("UP")
        for _ in range(0, abs(offset)):
            if offset > 0:
                moves.append("RIGHT")
            else:
                moves.append("LEFT")
        #moves.append('RETURN')
        parent.ai_executes_moves(moves)
        #return moves
