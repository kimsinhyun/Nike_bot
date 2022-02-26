import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from time import sleep
from driver_func.check_time import check_time

def time_trigger(start_hour, start_min, user_num):
    #타임 트리거 (예약 실행)
    if(start_hour != "0" or start_min != "0"):
        while True:
            if check_time(start_hour, start_min,user_num):
                print("start")
                sleep(0.8)
                break

# time_trigger("15","55")