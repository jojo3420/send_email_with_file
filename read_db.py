import os
from datetime import datetime, timedelta

import pymysql.cursors
import dotenv
import pandas as pd
from devtools import debug

from email_module import send_mail


def run():
    dotenv.load_dotenv('.env')
    # dateDict = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'}
    # Connect to the database
    conn = pymysql.connect(host=os.getenv('DB_HOST'),
                           user=os.getenv('DB_USERNAME'),
                           password=os.getenv('DB_PASSWORD'),
                           database=os.getenv('DB_SCHEMA'),
                           cursorclass=pymysql.cursors.DictCursor
                           )
    with conn:
        ymd_format = '%Y-%m-%d'
        today = datetime.today()
        diff = timedelta(days=1)
        yesterday = today - diff
        start, end = yesterday.strftime(ymd_format), today.strftime(ymd_format)

        path = f'./data/{start}'
        is_exist = os.path.exists(path)
        if is_exist is False:
            os.makedirs(path)

        with conn.cursor() as cursor:
            # weekday = datetime.today().weekday()
            # if weekday in [0]:
            sql = "SELECT created_at, username, mobile FROM user " \
                  "WHERE created_at BETWEEN %s AND %s"
            cursor.execute(sql, (start, end))
            rows: list = cursor.fetchall()
            df = pd.DataFrame(rows)
            df.to_csv(path + '/user.csv')

        with conn.cursor() as cursor:
            sql = "SELECT count(*) as cnt FROM kakao_history " \
                  " WHERE created_at BETWEEN %s AND %s "
            cursor.execute(sql, (start, end))
            row = cursor.fetchone()
            # print(start, row.get('cnt', 0))
            df = pd.Series({'date': start, 'count': row.get('cnt', 0)})
            df.to_csv(path + '/kakao_history.csv')

    user_file_path = path + '/user.csv'
    user_is_exist = os.path.exists(user_file_path)
    kakao_file_path = path + '/kakao_history.csv'
    kakao_is_exist = os.path.exists(kakao_file_path)
    print(user_is_exist, kakao_is_exist)

    me = 'jjjhhhvvv@naver.com'
    send_to = 'jongun.flow@gmail.com'
    _ = ''
    if user_is_exist and kakao_is_exist:
        send_mail(_, me,
                  f'isky 전일 통계데이터 첨부 {start} 자료',
                  '데이터 첨부.',
                  [user_file_path, kakao_file_path]
                  )
        debug('메일 전송 OK')
    else:
        send_mail(_, me, 'isky 전일 통계데이터 메일 전송 실패',
                  f'user_is_exist: {user_is_exist}, kakao_is_exist: {kakao_is_exist} '
                  f'\n파일 생성이 안되었다.',
                  []
                  )
        debug('메일 전송 FAIL')