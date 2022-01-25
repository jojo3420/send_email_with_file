import time
import threading


# 함수 정의, 함수 내부에 threading 정의
def printhello():
    print("Hello!")
    # threading을 정의한다. 5초마다 반복 수행함.
    threading.Timer(5, printhello).start()


# printhello
printhello()
