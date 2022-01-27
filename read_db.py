import os
from datetime import datetime, timedelta

import pymysql.cursors
import dotenv
import pandas as pd
from devtools import debug

from email_module import send_mail

columns = ['id', '이벤트 참여 시간', '이름', '전화번호', '유저 키', '카카오톡 공유 여부']

ymd_format = '%Y-%m-%d'
_today = datetime.today()
_diff = timedelta(days=1)
_yesterday = _today - _diff
yesterday, today = _yesterday.strftime(ymd_format), _today.strftime(ymd_format)


def read_data_and_save_excel():
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
        dir = f'./data/{today}'
        is_exist = os.path.exists(dir)
        if is_exist is False:
            os.makedirs(dir)
        with conn.cursor() as cursor:
            sql = "SELECT id, created_at, username, mobile, `identify` " \
                  " FROM user " \
                  " WHERE 1=1 " \
                  " ORDER BY created_at DESC"
            cursor.execute(sql)
            rows: list = cursor.fetchall()
            for row in rows:
                share_yn = 'N'
                # print(row) # row is dict
                identify = row.get('identify', '')
                if identify:
                    SQL = "SELECT `identify` " \
                          " FROM kakao_history " \
                          " WHERE log IS NOT NULL AND `identify` = %s "
                    cursor.execute(SQL, identify)
                    history_rows = cursor.fetchall()
                    if len(history_rows) > 0:
                        share_yn = "Y"
                row['share_kakao_link'] = share_yn
            file_path = f'{dir}/data_{today}.xlsx'
            df = pd.DataFrame(rows)
            df.columns = columns
            df.to_excel(
                file_path,
                index=False,
                encoding='UTF-8'
            )
            return file_path


def send(file_path):
    me = os.getenv('TO_EMAIL_ME')
    send_to_jo = os.getenv('TO_EMAIL_JO')
    send_to_client = os.getenv('TO_EMAIL_CLIENT')
    _ = ''
    if file_path is not None:
        send_mail(_, me,
                  f'아이스카이 공유이벤트 참여자 통계 {today}',
                  '파일 첨부',
                  [file_path]
                  )
        send_mail(_, send_to_jo,
                  f'아이스카이 공유이벤트 참여자 통계 {today}',
                  '파일 첨부',
                  [file_path]
                  )
        send_mail(_, send_to_client,
                  f'아이스카이 공유이벤트 참여자 통계 {today}',
                  '파일 첨부',
                  [file_path]
                  )

        debug('메일 전송 OK')
    else:
        send_mail(_, me, 'isky 전일 통계데이터 메일 전송 실패',
                  f'path: {file_path} '
                  f'\n파일 생성이 안되었다.',
                  []
                  )
        debug('메일 전송 FAIL')


