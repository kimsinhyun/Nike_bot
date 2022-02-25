from posixpath import abspath
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import chromedriver_autoinstaller
from time import sleep
import subprocess
import pandas as pd
from concurrent import futures
from driver_setting.user_info import get_user_info
from driver_setting.chrome_cookie_driver_exe import get_cookie_driver_exe
from driver_setting.set_chrome_options import get_chrome_options


user_info = pd.read_csv('../info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)

def init(user_num):
    #--------------------------아이디 패스워드 프록시 설정--------------------------
    ID, PW, PROXY, LINK, SIZE,proxy_dict =  get_user_info(user_info, user_num)
    proxy_port = proxy_dict['proxy_port']

    #크롬 버전
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    #쿠키, 드라이버 ,exe
    chrome_cookie_path, chrome_exe_path, chrome_driver_path = get_cookie_driver_exe(chrome_ver, user_num)
    
    #run chrome by subprocess
    process = subprocess.Popen(f'{chrome_exe_path} --remote-debugging-port={proxy_port} --user-data-dir="{chrome_cookie_path}"')

    #driver option
    capabilities, options = get_chrome_options(proxy_dict,proxy_port)
    driver = webdriver.Chrome(executable_path=f'..\{chrome_ver}\chromedriver.exe', desired_capabilities=capabilities, chrome_options=options)

    # driver = webdriver.Chrome(executable_path='.\98\chromedriver.exe', desired_capabilities=capabilities, chrome_options=options)
    #크롬 드라이버 설정
    try:
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    except:
        #크롬 드라이버 버전 관리
        chromedriver_autoinstaller.install(True)  
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    

    #크롬 드라이버 설정
    try:
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    except:
        #크롬 드라이버 버전 관리
        chromedriver_autoinstaller.install(True)  
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    
    driver.get("https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif?hl=en")
    temp_1 = input("enter any key to install ip check extension")
    driver.get("https://chrome.google.com/webstore/detail/website-ip/agbkjcoclkflcpkognkhjkllhimlpice/related")

    temp = input("enter any key to terminate: ")
    process.kill()
# 멀티 쓰레딩
with futures.ThreadPoolExecutor(max_workers=20) as executor: 
                                                                    #user_num을 바꿔서 원하는 쓰레드 개수를 지정할 수 있음)
    future_test_results = [ executor.submit(init, 0) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))