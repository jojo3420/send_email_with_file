import time
from read_db import run
from devtools import debug
import datetime as dt
from scheduler import Scheduler
import scheduler.trigger as trigger


# debug('프로그램시작')
# schedule.every(1).minutes.do(run)  # 1분마다 실행
# schedule.every().day.at("10:00").do(run)  # 매일 10시00분

# 실제 실행하게 하는 코드
# while True:
#     schedule.run_pending()
#     time.sleep(1)




TZ_KST = dt.timezone(dt.timedelta(hours=9))
schedule = Scheduler(tzinfo=dt.timezone.utc)

schedule.daily(dt.time(hour=10, tzinfo=TZ_KST), run)
print(schedule)

while True:
    schedule.exec_jobs()
    time.sleep(1)
