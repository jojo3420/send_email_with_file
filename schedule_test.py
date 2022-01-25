import time
import schedule


# 특정 함수 정의
def printhello():
    print("Hello!")


schedule.every(1).minutes.do(printhello)  # 1분마다 실행
# schedule.every().monday.at("00:10").do(printhello)  # 월요일 00:10분에 실행
# schedule.every().day.at("10:30").do(printhello)  # 매일 10시30분에

# 실제 실행하게 하는 코드
while True:
    schedule.run_pending()
    time.sleep(1)
