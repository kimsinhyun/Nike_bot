import sys
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import time
from concurrent import futures
import pandas as pd

from temp.setting import WebDriver, load_cookie, save_cookie
from driver_func.check_login import check_logged_in, login
from driver_func.user_info import get_user_info
from driver_func.show_ip import show_proxy_ip
from driver_func.time_trigger import time_trigger

user_info = pd.read_csv('../info.csv')
user_num = len(user_info)
input_hour = input("set hour: ")
input_min = input("set min: ")
check_ip = input("ip 확인 (건너뛰기: 'press any key' ; 확인하기: 'enter y or yes')")

def main(user_num):
     #몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
     ID, PW, PROXY, LINK, SIZE,proxy_dict =  get_user_info(user_info, user_num)

     user_proxy = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])
     driver= WebDriver(user_proxy,user_num)
     driverinstance = driver.driver_instance
     # load_cookie(driverinstance)
     # show ip
     show_proxy_ip(driver=driverinstance, hold_time=5, check_ip = check_ip)

     time_trigger(input_hour, input_min, user_num)



     driverinstance.get("https://www.nike.com/kr/ko_kr/") 
     # save_cookie(driverinstance)
     time.sleep(3)
     if(check_logged_in(driverinstance,user_num) == False):
          login(driverinstance,ID,PW, user_num)

     terminate = input("enter any key to terminate")
     terminate = input("enter any key to terminate")
     print("done")

with futures.ThreadPoolExecutor(max_workers=20) as executor: 
     future_test_results = [ executor.submit(main, i) for i in range(user_num) ] # running same test 6 times, using test number as url
     for future_test_result in future_test_results: 
          try:        
               test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
          except: # can give a exception in some thread, but 
               print('thread generated an exception: {:0}'.format(Exception))