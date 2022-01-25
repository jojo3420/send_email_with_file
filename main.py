import time
import schedule
from read_db import run
from devtools import debug

debug('프로그램시작')
schedule.every(1).minutes.do(run)  # 1분마다 실행
# schedule.every().day.at("10:00").do(run)  # 매일 10시00분

# 실제 실행하게 하는 코드
while True:
    schedule.run_pending()
    time.sleep(1)


