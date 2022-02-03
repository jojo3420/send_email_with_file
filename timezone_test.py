import datetime as dt
from pytz import timezone

KR_TZ = timezone("Asia/Seoul")

print(dt.datetime.now(KR_TZ))