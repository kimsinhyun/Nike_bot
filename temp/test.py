import warnings

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time
from concurrent import futures
import pandas as pd

from setting import WebDriver
from driver_func.check_login import check_logged_in, login
from driver_func.user_info import get_user_info
from driver_func.show_ip import show_proxy_ip
from driver_func.time_trigger import time_trigger
from driver_func.workflow import first_step,second_step,thrid_step
from driver_func.check_day import check_day



warnings.filterwarnings(action='ignore')

user_info = pd.read_csv('info.csv')
user_num = len(user_info)
check_ip = input("ip 확인 (건너뛰기: 'press any key' ; 확인하기: 'enter y or yes')")
input_hour = input("set hour: ")
input_min = input("set min: ")
retry_time = int(input("set retry time(second): "))



def init(user_num):

     if(check_day() == False):
          print("error")
          return

     #몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
     ID, PW, PROXY, LINK, SIZE,proxy_dict =  get_user_info(user_info, user_num)

     user_proxy = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])
     driver= WebDriver(user_proxy,user_num)
     driverinstance = driver.driver_instance

     # show ip
     show_proxy_ip(driver=driverinstance, hold_time=5, check_ip = check_ip)

     driverinstance.get("https://www.nike.com/kr/ko_kr/") 

     if(check_logged_in(driverinstance,user_num) == False):
          login(driverinstance,ID,PW, user_num)
     
     driverinstance.set_window_size(900, 600)
     # driverinstance.set_window_size(480, 320)

     time_trigger(input_hour, input_min, user_num)

     job_condition = "choose_size"
     for i in range(10):
          if(job_condition=="choose_size"):
               #첫 시도는 희망하는 사이즈로 선택
               get_size_mode = "select_size"
               #first_step -> 사이즈 서택 페이지, 성공하면 choose_address를 return 받아서 다음 스텝으로 넘어간다.
               job_condition = first_step(driverinstance, LINK, SIZE, get_size_mode, retry_time,job_condition)

          if(job_condition=="choose address"):
               job_condition = second_step(driverinstance,job_condition)

          if(job_condition=="choose_payment"):
               job_condition = thrid_step(driverinstance,user_num, LINK,SIZE,get_size_mode, job_condition)

          if(job_condition == "finish"):
               break

     temp = input("아무 키를 눌러서 종료해주세요 ")
     temp_1 = input("정말 종료 하시겠습니까? (아무 키 입력)")

def main():
     print(user_info)
     with futures.ThreadPoolExecutor(max_workers=50) as executor: 
          future_test_results = [ executor.submit(init, i) for i in range(user_num) ] # running same test 6 times, using test number as url
          for future_test_result in future_test_results: 
               try:        
                    test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
               except: # can give a exception in some thread, but 
                    print('thread generated an exception: {:0}'.format(Exception))

     time.sleep(10)

if __name__ == "__main__":
    main()