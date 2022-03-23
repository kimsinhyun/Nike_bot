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

def init(user_num):
     ID, PW, PROXY, LINK, SIZE,proxy_dict =  get_user_info(user_info, user_num)
     if(check_day() == False):
          print("error")
          return

     #몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
     user_proxy = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])
     driver= WebDriver(user_proxy,user_num)
     driverinstance = driver.driver_instance

     # show ip
     show_proxy_ip(driver=driverinstance, hold_time=5, check_ip = check_ip)

     driverinstance.get("https://www.nike.com/kr/ko_kr/") 

     if(check_logged_in(driverinstance,user_num) == False):
          login(driverinstance,ID,PW, user_num)

     return driverinstance

def start_ko_kr(user_num, ko_kr_link, driverinstance):
     print(ko_kr_link)
     ID, PW, PROXY, LINK, SIZE,proxy_dict =  get_user_info(user_info, user_num)
     job_condition = "choose_size"
     for i in range(10):
          if(job_condition=="choose_size"):
               #첫 시도는 희망하는 사이즈로 선택
               get_size_mode = "select_size"
               #first_step -> 사이즈 서택 페이지, 성공하면 choose_address를 return 받아서 다음 스텝으로 넘어간다.
               job_condition = first_step(driverinstance, ko_kr_link, SIZE, get_size_mode, job_condition)

          if(job_condition=="choose address"):
               job_condition = second_step(driverinstance,job_condition)

          if(job_condition=="choose_payment"):
               job_condition = thrid_step(driverinstance,user_num, ko_kr_link,SIZE,get_size_mode, job_condition)

          if(job_condition == "finish"):
               break

     temp = input("아무 키를 눌러서 종료해주세요 ")
     temp_1 = input("정말 종료 하시겠습니까? (아무 키 입력)")
     return
     
def main():
     print(user_info)
     Webdriver_list = [0 for i in range(user_num)]
     with futures.ThreadPoolExecutor(max_workers=50) as executor: 
          future_test_results = [ executor.submit(init, i) for i in range(user_num) ] # running same test 6 times, using test number as url
          for i, future_test_result in enumerate(future_test_results): 
               try:        
                    test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
                    Webdriver_list[i] = test_result
               except: # can give a exception in some thread, but 
                    print('thread generated an exception: {:0}'.format(Exception))

          #입력
          print("모든 창이 준비완료 됐습니다")
          ko_kr_link = input("ko_kr 링크를 입력해주세요: ")
          ko_kr_link_results = [ executor.submit(start_ko_kr, i, ko_kr_link, Webdriver_list[i]) for i in range(user_num) ] # running same test 6 times, using test number as url
          for ko_kr_link_result in ko_kr_link_results: 
               try:        
                    test_result = ko_kr_link_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
               except: # can give a exception in some thread, but 
                    print('thread generated an exception: {:0}'.format(Exception))

     time.sleep(10)

if __name__ == "__main__":
    main()