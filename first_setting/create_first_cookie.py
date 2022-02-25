from posixpath import abspath
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from time import sleep
import pandas as pd
from concurrent import futures
from driver_setting.combinate_settings_to_one_driver import execute_subprocess_and_return_driver
from driver_setting.user_info import get_user_info
from driver_setting.chrome_cookie_driver_exe import get_cookie_driver_exe
from driver_setting.set_chrome_options import get_chrome_options


user_info = pd.read_csv('../info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)

def init(user_num):
    #--------------------------아이디 패스워드 프록시 설정--------------------------
    ID, PW, PROXY, LINK, SIZE,proxy_dict =  get_user_info(user_info, user_num)

    #크롬 드라이버 설정
    driver,_ = execute_subprocess_and_return_driver(user_info,user_num)
    
    driver.get("https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif?hl=en")

# 멀티 쓰레딩
with futures.ThreadPoolExecutor(max_workers=20) as executor: 
    future_test_results = [ executor.submit(init, 0) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))