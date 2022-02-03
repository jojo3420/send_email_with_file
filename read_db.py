import os
import time
from datetime import datetime, timedelta
import pymysql.cursors
import dotenv
import pandas as pd
from devtools import debug

from email_module import send_mail

columns = ['id', '이벤트 참여 시간', '이름', '전화번호', '유저 키', '카카오톡 공유 여부']


def read_data_and_save_excel():
    today = time.strftime('%Y-%m-%d')

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
            writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

            # sheet1
            df = pd.DataFrame(rows)
            df.columns = columns

            # sheet2
            sql2 = "SELECT date_format(created_at, '%Y-%m-%d') AS day, " \
                   " COUNT(created_at) AS cnt " \
                   " FROM kakao_history " \
                   " GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d')"
            cursor.execute(sql2)
            rows2 = cursor.fetchall()
            df2 = pd.DataFrame(rows2)
            df2.columns = ['날짜', '카카오톡 공유인원']

            sql3 = 'SELECT id, created_at,  identify FROM kakao_history ORDER BY id DESC'
            cursor.execute(sql3)
            rows3 = cursor.fetchall()
            df3 = pd.DataFrame(rows3)
            df3.columns = ['id', '날짜', '유저 키']

            df.to_excel(
                writer,
                index=False,
                encoding='UTF-8',
                sheet_name="이벤트 참여"
            )
            df2.to_excel(
                writer,
                index=False,
                encoding='UTF-8',
                sheet_name="날짜별 공유인원"
            )
            df3.to_excel(
                writer,
                index=False,
                encoding='UTF-8',
                sheet_name="공유 완료 정보"
            )
            writer.save()
            return file_path


def send(file_path):
    today = time.strftime('%Y-%m-%d %H:%M:%S')
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


read_data_and_save_excel()
