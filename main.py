import time
from read_db import read_data_and_save_excel, send
from devtools import debug
import datetime as dt
from scheduler import Scheduler
import scheduler.trigger as trigger

print('프로그램시작')

TZ_KST = dt.timezone(dt.timedelta(hours=9))
schedule = Scheduler(tzinfo=dt.timezone.utc)


def run():
    file_path = read_data_and_save_excel()
    print(file_path)
    if file_path:
        send(file_path)


schedule.daily(dt.time(hour=17, minute=50, tzinfo=TZ_KST), run)
print(schedule)

while True:
    schedule.exec_jobs()
    time.sleep(1)
