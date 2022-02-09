#!/usr/bin/env python
# coding: utf-8

# In[1]:


from concurrent import futures

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.support.ui import WebDriverWait as wait 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from time import sleep
import time

import os

#버전 관리용 라이브러리
import chromedriver_autoinstaller

import subprocess
import shutil

import datetime
from pytz import timezone

import pyperclip

import pandas as pd


# # 디버깅 용

# In[2]:


user_info = pd.read_csv('./info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)
user_info


# # 실제 로그인 코드

# In[7]:


# def selenium_test(test_url):
#     chromeOptions = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=caps, options=option)
#     sleep(20)

def init(user_num):
    #--------------------------아이디 패스워드 프록시 설정--------------------------
    ID = str(user_info[user_info['DIR_NUM']==user_num]['ID'].values[0])
    PW = str(user_info[user_info['DIR_NUM']==user_num]['PW'].values[0])
    PROXY = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])
    
    #--------------------------아이디 패스워드 프록시 설정--------------------------

    #------------크롬 버전 확인 및 각 사용자별 exe파일 경로 및 쿠키 경로------------
#     chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    chrome_ver = '97'

    chrome_exe_path = str(os.path.abspath(os.getcwd()))
    chrome_exe_path = chrome_exe_path.replace('\개발용dir','')
    chrome_exe_path = chrome_exe_path + "\\" +str(user_num)  + '\Chrome\Application\chrome.exe'

    chrome_cookie_path = str(os.path.abspath(os.getcwd()))
    chrome_cookie_path = chrome_cookie_path.replace('\개발용dir','')
    chrome_cookie_path = chrome_cookie_path + "\\" +str(user_num) + '\Chrome_cookie'

    chrome_driver_path = str(os.path.abspath(os.getcwd()))
    chrome_driver_path = chrome_driver_path.replace('\개발용dir','')
    chrome_driver_path = chrome_driver_path + "\\" +str(user_num) + '\\' + chrome_ver + '\chromedriver.exe'
    #------------크롬 버전 확인 및 각 사용자별 exe파일 경로 및 쿠키 경로------------
    
    port_num = 9222 + user_num
    #------------------------자동 제어모드 우회------------------------------
    subprocess.Popen(r'{exe} --remote-debugging-port={port_num} --user-data-dir="{cookie}"'.format(exe=chrome_exe_path, cookie=chrome_cookie_path, port_num=str(port_num)))
    #------------------------자동 제어모드 우회------------------------------
    
    
    #---------------------------프록시 서버 설정------------------------------
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL"
    }

    #페이지가 다 로드 되기 전에 다음 코드 실행할 수 있도록 설정
    caps = DesiredCapabilities().CHROME 
    caps["pageLoadStrategy"] = "none"

    #디버거 모드로 설정(이렇게 안하면 로그인이 다 막힘)
    option = Options()
    option.add_argument("--start-maximized")
    option.add_experimental_option("debuggerAddress", f"127.0.0.1:{port_num}")
    option.add_argument('--blink-settings=imagesEnabled=false')
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
    option.add_argument(f'--user-data-dir={chrome_cookie_path}')


    #크롬 드라이버 설정
    try:
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=caps, options=option)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=caps, options=option)
    
    print(chrome_exe_path)
    driver.implicitly_wait(3)  
    driver.get("https://www.nike.com/kr/ko_kr/")
    sleep(10)
    driver.get("https://www.nike.com/kr/ko_kr/t/men/fw/basketball/DH6931-001/kvzw69/air-jordan-1-low-se")
    sleep(10)
#     driver.switch_to.window(driver.window_handles[0])
    
    
with futures.ThreadPoolExecutor(max_workers=20) as executor: 
    future_test_results = [ executor.submit(init, i) for i in range(3) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
            #... do something with the test_result
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




