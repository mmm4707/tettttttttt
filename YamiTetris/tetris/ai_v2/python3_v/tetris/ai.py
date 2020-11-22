from ai_field import ai_Field
import copy

#블럭을 시계방향으로 회전시켜 주기
def ai_rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]


#AI를 만들어주는 클래스
class Ai:

    @staticmethod
    #   best(ai_field, [piece, next_piece], 0, weights, 1)
    def best(ai_field, workingPieces, workingPieceIndex, weights, ai_level):
        bestRotation = None
        bestOffset = None
        bestScore = -10000 #초기 값
        #현재 작업중인 블럭의 인덱스 ( 0 )
        workingPieceIndex = copy.deepcopy(workingPieceIndex)

        #작업중인 블럭"들" 중에 인덱스 (0)에 해당하는   인덱스 0 번째가  진짜 내려가는 놈임
        workingPiece = workingPieces[workingPieceIndex]

        #모양 변화 ??
        shapes_rotation = { 4 : 4, 8 : 2, 12 : 2, 16 : 4, 20 : 4, 24 : 2, 28 : 1 }

        #블럭을 납짝만두로 만들어 버리기
        #현재 내려가고 있는 있는 블럭의  값들을    리스트 하나에 일렬로 나열해준다.
        flat_piece = [val for sublist in workingPiece for val in sublist]
        # 나열한 모든 값들을 더해준다...?  !! 블럭 보양에 따라 그 값이 달라진다.( 총개수, 모양, 색표시 위한 val 값 때문)
        hashedPiece = sum(flat_piece)


        #각 열에서 시작해서, 모양을 변화 시켜가면 블럭을 내려, 점수가 높게 나오는  위치, 회전수 구하기
        # 납짝 만두의 값에 해당하는 dictionary값만큼 반복,  각가 회전 반복수는
        for rotation in range(0, shapes_rotation[hashedPiece]):
            #열의 개수만큼 반복(10) 그럼 각열을 안에서 offset이라 부르기
            for offset in range(0, ai_field.ai_width):

                #결과는 변환된 보드 그 자체를 반환 해줌,  특정 조건에서는 false 반환
                result = ai_field.projectPieceDown(workingPiece, offset, ai_level)
                if not result is None: # none말고 보드 자체를 받으면
                    score = None #점수는 초기화!

                    #지금 작업중인 index가(0)  == (1) 이면   (다음 블럭이 없다면??)
                    if workingPieceIndex == len(workingPieces)-1 :
                        #weight에 해당 하는 값들을 return 해주는 것을 받아온다.
                        heuristics = ai_field.heuristics()
                        #점수 = 가각의 특성값 * weight값이 된다.
                        score = sum([a*b for a,b in zip(heuristics, weights)])

                    #
                    else:
                        _, _, score = Ai.best(ai_field, workingPieces, workingPieceIndex + 1, weights, 2)

                    # 위에서 나온 점수가, 가장 좋은 점수보다 높다면
                    #그 값들을  모두 최신화 시켜주기
                    if score > bestScore :
                        bestScore = score
                        bestOffset = offset
                        bestRotation = rotation
                ai_field.undo(ai_level)
            #내려가고 있는 블럭 회전 시키기 (각 블럭마다 정해진 회전 수가 있음)
            workingPiece = ai_rotate_clockwise(workingPiece)
        #위와 같이 각 위치당 회전시키면 내렸을때, 점수가 가장 높아 지는 것들 골라내기
        return bestOffset, bestRotation, bestScore


    @staticmethod
    def choose(initialField, piece, next_piece, offsetX, weights, parent):

        # ai 필드 지정해 주기  initialfiled에서는 ai_board를 받음,   ai 보드를 통해 field 생성   [10 , 18] 열개수, 행 개수 넘겨주기
        ai_field = ai_Field(len(initialField[0]), len(initialField))
        #받은 필드를 복사해서 업데이트 하기
        ai_field.updateField(copy.deepcopy(initialField))

        #위서 고른 가장 좋은  상태의 시작점, 회전수를 받아온다.
        offset, rotation, _ = Ai.best(ai_field, [piece, next_piece], 0, weights, 1)
        moves = []

        offset = offset - offsetX  # 블럭 내려 오는 위치를 보드의 가운데로 맞추는 작업
        for _ in range(0, rotation):
            moves.append("UP")
        for _ in range(0, abs(offset)):
            if offset > 0:
                moves.append("RIGHT")
            else:
                moves.append("LEFT")
        #moves.append('RETURN')
        # 객체의 움직임을 등록
        parent.ai_executes_moves(moves)
        return moves
