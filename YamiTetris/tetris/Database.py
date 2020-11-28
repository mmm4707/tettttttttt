import pymysql


class Database:
    def __init__(self):
        self.score_db = pymysql.connect(
        user = 'yutan0565',
        passwd = '12345678', # 데이터 서버 비밀번호는 나만 알음...  #요거 문제 해겨 하긴 해야함
        host = 'db-tetris.cn66pqzgn9vt.ap-northeast-2.rds.amazonaws.com',
        db = 'TetrisDB',
        charset = 'utf8'
        )


    def load_data(self, game_mode):
        #불러 오기
        curs = self.score_db.cursor(pymysql.cursors.DictCursor)
        if game_mode == 'original':
            sql = "select * from original_score order by score desc "
        elif game_mode == 'twohands':
            sql = "select * from twohands_score order by score desc"
        elif game_mode == 'mini':
            sql = "select * from mini_score order by score desc"
        curs.execute(sql)
        data = curs.fetchall() #리스트 안에 딕셔너리가 있는 형태

        return data

    def add_data(self,game_mode,  ID, score):
        #추가하기
        curs = self.score_db.cursor()
        if game_mode == 'original':
            sql = "INSERT INTO original_score (ID, score) VALUES (%s, %s)"
        elif game_mode == 'twohands':
            sql = "INSERT INTO twohands_score (ID, score) VALUES (%s, %s)"
        elif game_mode == 'mini':
            sql = "INSERT INTO mini_score (ID, score) VALUES (%s, %s)"
        curs.execute(sql, (ID, score))
        self.score_db.commit()  #서버로 추가 사항 보내기


