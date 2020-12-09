import copy
from variable import Var


class Ai:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[Var.board_empty_state] * self.width] * self.height

    def size(self):
        return self.width, self.height

    def updateField(self, field):
        self.field = field

    @staticmethod
    def check_collision(field, shape, offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and field[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False

    def projectPieceDown(self, piece, offsetX, workingPieceIndex):
        if offsetX + len(Var.piece_length(piece)) > self.width or offsetX < Var.board_start_x:
            return None
        # result = copy.deepcopy(self)
        offsetY = self.height
        for y in range(Var.board_start_y, self.height):
            if Ai.check_collision(self.field, piece, (offsetX, y)):
                offsetY = y
                break
        for x in range(Var.block_start_index, len(Var.piece_length(piece))):
            for y in range(Var.block_start_index, len(piece)):
                value = piece[y][x]
                if value > Var.board_empty_state:
                    self.field[offsetY - Var.for_index_var + y][offsetX + x] = -workingPieceIndex
        return self

    def undo(self, workingPieceIndex):
        self.field = [[Var.board_empty_state if el == -workingPieceIndex else el for el in row] for row in self.field]

    def heightForColumn(self, column):
        width, height = self.size()
        for i in range(Var.board_start_y, height):
            if self.field[i][column] != Var.board_empty_state:
                return height - i
        return Var.board_empty_state

    def heights(self):
        result = []
        width, height = self.size()
        for i in range(Var.board_start_x, width):
            result.append(self.heightForColumn(i))
        return result

    ################################################
    #                   HEURISTICS                 #
    ################################################

    def heuristics(self):
        heights = self.heights()
        maxColumn = self.maxHeightColumns(heights)
        return heights + [self.aggregateHeight(heights)] + self.numberOfHoles(heights) + self.bumpinesses(heights) + [
            self.completLine(), self.maxPitDepth(heights), self.maxHeightColumns(heights),
            self.minHeightColumns(heights)]

    def aggregateHeight(self, heights):
        result = sum(heights)
        return result

    def completLine(self):
        result = Var.ai_initial_completLine
        width, height = self.size()
        for i in range(Var.board_start_y, height):
            if Var.board_empty_state not in self.field[i]:
                result += Var.ai_count_completLine
        return result

    def bumpinesses(self, heights):
        result = []
        for i in range(Var.board_start_y, len(heights) - Var.for_index_var):
            result.append(abs(heights[i] - heights[i + Var.for_index_var]))
        return result

    def numberOfHoles(self, heights):
        results = []
        width, height = self.size()
        for j in range(Var.board_start_x, width):
            result = Var.ai_initial_numberOfHoles
            for i in range(Var.board_start_y, height):
                if self.field[i][j] == Var.board_empty_state and height - i < heights[j]:
                    result += Var.ai_count_numberOfHoles
            results.append(result)
        return results

    def maxHeightColumns(self, heights):
        return max(heights)

    def minHeightColumns(self, heights):
        return min(heights)

    def maxPitDepth(self, heights):
        return max(heights) - min(heights)

    def rotate_clockwise(shape):  # 회전 시킨 모양 만들어 주기
        return [[shape[y][x]
                 for y in range(len(shape))]
                for x in range(len(Var.piece_length(shape)) - Var.for_index_var, Var.search_rotate_next_index,
                               Var.last_rotate_index_prev)]

    ########################3
    @staticmethod
    def best(field, workingPieces, workingPieceIndex, weights, level):
        bestRotation = None
        bestOffset = None
        bestScore = Var.ai_initial_bestscore
        workingPieceIndex = copy.deepcopy(workingPieceIndex)
        workingPiece = workingPieces[workingPieceIndex]
        flat_piece = [val for sublist in workingPiece for val in sublist]
        hashedPiece = sum(flat_piece)
        for rotation in range(Var.rotate_start, Var.shapes_rotation[hashedPiece]):
            for offset in range(Var.board_start_x, field.width):
                result = field.projectPieceDown(workingPiece, offset, level)
                if not result is None:
                    score = None
                    if workingPieceIndex == len(workingPieces) - Var.for_index_var:
                        heuristics = field.heuristics()
                        score = sum([a * b for a, b in zip(heuristics, weights)])
                    else:
                        _, _, score = Ai.best(field, workingPieces, workingPieceIndex + Var.for_index_var, weights,
                                              Var.ai_best_fix_level)

                    if score > bestScore:
                        bestScore = score
                        bestOffset = offset
                        bestRotation = rotation
                field.undo(level)
            workingPiece = Ai.rotate_clockwise(workingPiece)

        return bestOffset, bestRotation, bestScore

    @staticmethod
    def choose(initialField, piece, next_piece, offsetX, weights, parent):
        field = Ai(len(initialField[Var.field_up_line]), len(initialField))
        field.updateField(copy.deepcopy(initialField))

        offset, rotation, _ = Ai.best(field, [piece, next_piece], Var.ai_working_piece_index, weights,
                                      Var.ai_choice_fix_level)
        moves = []

        offset = offset - offsetX
        for _ in range(Var.rotate_start, rotation):
            moves.append("UP")
        for _ in range(Var.board_start_x, abs(offset)):
            if offset > Var.board_start_x:
                moves.append("RIGHT")
            else:
                moves.append("LEFT")
        # moves.append('RETURN')
        parent.ai_executes_moves(moves)
        # return moves

