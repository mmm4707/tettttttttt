import copy



class ai_Field:
    def __init__(self, ai_width, ai_height):    # 열개수(10), 행개수(18) 받아오기
        self.ai_width = ai_width        #내부 변수에 할당  - 열개수
        self.ai_height = ai_height      # 행개수
        self.ai_field = [[0]*self.ai_width]*self.ai_height    #ai_field는   모두 0으로 초반에 채워 넣기  (ai_board와 비슷한 것)  (18 * 10)의 매트릭스 만들기

    #열개수, 행개수 반환
    def size(self):
        return self.ai_width, self.ai_height

    #받아온 ai_field를 반환
    def updateField(self, ai_field):
        self.ai_field = ai_field

    @staticmethod
    #충돌 체크
    def check_collision(ai_field, shape, ai_offset):
        off_x, off_y = ai_offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and ai_field[ cy + off_y ][ cx + off_x ]:
                        return True
                except IndexError:
                    return True
        return False

    # 블럭이 내려가는 모습 보여주기 (현재 움직이는 블럭, 열 번째, ai+level...?
    def projectPieceDown(self, piece, offsetX, workingPieceIndex):
        #  열번째 + 현재움직이는 블럭의 가로 셀 수   >  10    또는 열번재가 0보다 작으면
        if offsetX+len(piece[0]) > self.ai_width or offsetX < 0:
            #false반환
            return None
        #result = copy.deepcopy(self)
        offsetY = self.ai_height
        for y in range(0, self.ai_height):
            if ai_Field.check_collision(self.ai_field, piece, (offsetX, y)):
                offsetY = y
                break
        for x in range(0, len(piece[0])):
            for y in range(0, len(piece)):
                value = piece[y][x]
                if value > 0:
                    self.ai_field[offsetY-1+y][offsetX+x] = -workingPieceIndex
        return self

    def undo(self, workingPieceIndex):
        self.ai_field = [[0 if el == -workingPieceIndex else el for el in row] for row in self.ai_field]

    def heightForColumn(self, ai_column):
        ai_width, ai_height = self.size()
        for i in range(0, ai_height):
            if self.ai_field[i][ai_column] != 0:
                return ai_height-i
        return 0

    def ai_heights(self):
        ai_result = []
        ai_width, ai_height = self.size()
        for i in range(0, ai_width):
            ai_result.append(self.heightForColumn(i))
        return ai_result

    def numberOfHoleInColumn(self, ai_column):
        ai_result = 0
        maxHeight = self.heightForColumn(ai_column)
        for height, line in enumerate(reversed(self.ai_field)):
            if height > maxHeight: break
            if line[ai_column] == 0 and height < maxHeight:
                ai_result+=1
        return ai_result

    def numberOfHoleInRow(self, line):
        ai_result = 0
        for index, value in enumerate(self.ai_field[self.ai_height-1-line]):
            if value == 0 and self.heightForColumn(index) > line:
                ai_result += 1
        return ai_result

    ################################################
    #                   HEURISTICS                 #
    ################################################

    def heuristics(self):
        ai_heights = self.ai_heights()
        maxColumn = self.maxHeightColumns(ai_heights)
        return ai_heights + [self.aggregateHeight(ai_heights)] + self.numberOfHoles(ai_heights) + self.bumpinesses(ai_heights) + [self.completLine(), self.maxPitDepth(ai_heights), self.maxHeightColumns(ai_heights), self.minHeightColumns(ai_heights)]



    def aggregateHeight(self, ai_heights):
        ai_result = sum(ai_heights)
        return ai_result

    def completLine(self):
        ai_result = 0
        ai_width, ai_height = self.size()
        for i in range (0, ai_height) :
            if 0 not in self.ai_field[i]:
                ai_result+=1
        return ai_result

    def bumpinesses(self, ai_heights):
        ai_result = []
        for i in range(0, len(ai_heights)-1):
            ai_result.append(abs(ai_heights[i]-ai_heights[i+1]))
        return ai_result

    def numberOfHoles(self, ai_heights):
        ai_results = []
        ai_width, ai_height = self.size()
        for j in range(0, ai_width) :
            ai_result = 0
            for i in range (0, ai_height) :
                if self.ai_field[i][j] == 0 and ai_height-i < ai_heights[j]:
                    ai_result+=1
            ai_results.append(ai_result)
        return ai_results

    def maxHeightColumns(self, ai_heights):
        return max(ai_heights)

    def minHeightColumns(self, ai_heights):
        return min(ai_heights)

    def maximumHoleHeight(self, ai_heights):
        if self.numberOfHole(ai_heights) == 0:
            return 0
        else:
            maxHeight = 0
            for ai_height, line in enumerate(reversed(self.ai_field)):
                if sum(line) == 0: break
                if self.numberOfHoleInRow(ai_height) > 0:
                    maxHeight = ai_height
            return maxHeight

    def rowsWithHoles(self, maxColumn):
        ai_result = 0
        for line in range(0, maxColumn):
            if self.numberOfHoleInRow(line) > 0:
                ai_result += 1
        return ai_result

    def maxPitDepth(self, ai_heights):
        return max(ai_heights)-min(ai_heights)



    @staticmethod
    def __offsetPiece(piecePositions, ai_offset):
        piece = copy.deepcopy(piecePositions)
        for pos in piece:
            pos[0] += ai_offset[0]
            pos[1] += ai_offset[1]

        return piece

    def __checkIfPieceFits(self, piecePositions):
        for x,y in piecePositions:
            if 0 <= x < self.ai_width and 0 <= y < self.ai_height:
                if self.ai_field[y][x] >= 1:
                    return False
            else:
                return False
        return True

    def fitPiece(self, piecePositions, ai_offset=None):
        if ai_offset:
            piece = self.__offsetPiece(piecePositions, ai_offset)
        else:
            piece = piecePositions

        ai_field = copy.deepcopy(self.ai_field)
        if self.__checkIfPieceFits(piece):
            for x,y in piece:
                ai_field[y][x] = 1

            return ai_field
        else:
            return None
