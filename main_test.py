#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install pyperclip
# !pip install pytz
# !pip install schedule
# !pip install pause


# In[1]:


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


# In[2]:


# -------------------------------------------------
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

chrome_exe_path = str(os.path.abspath(os.getcwd()))
chrome_exe_path = chrome_exe_path + '\Chrome\Application\chrome.exe'

chrome_cookie_path = str(os.path.abspath(os.getcwd()))
chrome_cookie_path = chrome_cookie_path + '\Chrome_cookie'

chrome_driver_path = str(os.path.abspath(os.getcwd()))
chrome_driver_path = chrome_driver_path + '\\' + chrome_ver + '\chromedriver.exe'
# -------------------------------------------------
subprocess.Popen(r'{exe} --remote-debugging-port=9222 --user-data-dir="{cookie}"'.format(exe=chrome_exe_path, cookie=chrome_cookie_path))

#프록시 서버 설정
PROXY = "209.61.207.133:58758:run:rKeLShPi"
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
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# option.add_argument('--blink-settings=imagesEnabled=false')
option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
option.add_argument(f'--user-data-dir={chrome_cookie_path}')


#크롬 드라이버 설정
try:
    driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=caps, options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=caps, options=option)

#암시적 wait 설정
driver.implicitly_wait(1)    
    
#wait driver 설정
wait = WebDriverWait(driver, 6)

driver.get("https://www.nike.com/kr/ko_kr/")
driver.switch_to.window(driver.window_handles[0])


execute_time = input("실행 시간을 입력해주세요 ex) 10:00AM  : ")
item_link = input("상품 링크를 입력해주세요 ")
item_size = input("구매하실 상품의 사이즈를 입력해주세요: ")
item_num = int(input("구매하실 상품의 개수를 입력해주세요: "))

# execute_time = "8:57PM"
# item_link = 'https://www.nike.com/kr/ko_kr/t/men/fw/basketball/DA8026-017/jnnd14/jordan-series-mid'
# item_size = 265
# item_num = 1


while 1:
    start_program = input("먼저 로그인을 해주세요, 로그인 후 동작을 실행하려면 start 혹은 s를 입력 후 enter를 눌러주세요: ")
    if((start_program == 's') or (start_program == 'start')):
        break
    else:
        print('잘못된 입력입니다, 다시 입력해주세요')
        
def wait_untill(execute_time):
    if(execute_time != 0):
        sleep_until = execute_time # Sets the time to sleep until.
        sleep_until = time.strftime("%m/%d/%Y " + sleep_until, time.localtime()) # Adds todays date to the string sleep_until.
        now_epoch = time.time() #Current time in seconds from the epoch time.
        alarm_epoch = time.mktime(time.strptime(sleep_until, "%m/%d/%Y %I:%M%p")) # Sleep_until time in seconds from the epoch time.
        time.sleep(alarm_epoch - now_epoch + 0.7) # Sleeps until the next time the time is the set time, whether it's today or tomorrow.
    else:
        print("execute_time null")
    
    
def go_to_link(item_link):
    driver.get(item_link)


def click_item():
    action = ActionChains(driver)
    #검색해서 나온 페이지에서 첫 번째 아이템 클릭
    element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/section/section/section/article/div/div/ul/li[1]')))
    action.move_to_element(element).click().perform()
    
def click_size(item_size):
    action = ActionChains(driver)
    sleep(1.3)
    size_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,                         '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[1]/div/span[*]/label[text()=' + item_size  + ']')))
    action.move_to_element(size_element).click().perform()
    
def select_item_num(item_num):
    action = ActionChains(driver)
    try:
        item_num_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[5]/span/button[2]/i')))
    except:
        item_num_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[4]/span/button[2]/i')))
        
    action.move_to_element(item_num_element)
    for i in range(item_num-1):
        action.click().perform()
        sleep(0.05)

def check_size_selected_successfully():
    return driver.page_source.find("사이즈를 선택해 주세요")
  
def click_Purchase_btn():
    action = ActionChains(driver)
    Purchase_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-buy"]')))
    action.move_to_element(Purchase_btn).click().perform()
    
def choose_address():
    action = ActionChains(driver)
    default_addr = WebDriverWait(driver,4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="shipping_info"]/div[1]/ul/li[3]/div/span/label/i')))
    action.move_to_element(default_addr).click().perform()
    sleep(0.05)
    next_stage = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-next"]')))
    action.move_to_element(next_stage).click().perform()

def choose_payment():
    action = ActionChains(driver)
    payment = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="payment-review"]/div[1]/ul/li[1]/div/div[1]/h6/img')))
    action.move_to_element(payment).click().perform()
    sleep(0.05)
    terms_of_conditions = WebDriverWait(driver,2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="payment-review"]/div[1]/ul/li[2]/form/div/span/label/i')))
    action.move_to_element(terms_of_conditions).click().perform()
    sleep(1)
    complete_purchase = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="complete_checkout"]/button')))
    action.move_to_element(complete_purchase).click().perform()
    
    
def goto_cart():
    driver.get("https://www.nike.com/kr/ko_kr/cart")
    action = ActionChains(driver)
    cart_purchase = WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/section/section/article/div[2]/div[2]/div[1]/a')))
    action.move_to_element(cart_purchase).click().perform()
    
    
def job():
    if(execute_time!="0"):
        wait_untill(execute_time)
    #--------제품 링크로 이동--------
    go_to_link(item_link)
    #--------제품 검색 및 선택--------
    
    #--------개수 및 사이즈 선택--------
    while 1:
#         select_item_num(item_num)
        sleep(1)
        click_size(item_size)
        click_Purchase_btn()
        sleep(0.5)
        if(check_size_selected_successfully() == -1):
            break
        else:
            driver.refresh()
            pass
    #--------개수 및 사이즈 선택--------
    
    #--------결제--------
    choose_address()
    try:
        choose_payment()
    except:
        if(driver.current_url.find("no-access") != -1):
            goto_cart()
    if(driver.current_url.find("no-access") != -1):
        goto_cart()
    
    #--------결제--------

# /html/body/section/section/section/article/div[2]/div[2]/div[1]/a
job()


# In[ ]:


조던 시리즈 미드


# In[3]:


print(chrome_driver_path)


# In[ ]:


https://www.nike.com/kr/ko_kr/t/men/fw/basketball/DA8026-017/jnnd14/jordan-series-mid


# In[7]:


https://www.nike.com/kr/ko_kr/t/men/fw/nike-sportswear/DJ6188-001/mufe60/nike-dunk-low-retro


# In[5]:


item_num_element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[4]/span/button[2]/i')))


# In[3]:


from concurrent import futures
from selenium import webdriver


def selenium_test(test_url):
    chromeOptions = webdriver.ChromeOptions()
    #chromeOptions.add_argument("--headless") # make it not visible
    
    sleep(20)
with futures.ThreadPoolExecutor(max_workers=20) as executor: 
    future_test_results = [ executor.submit(selenium_test, i) for i in range(2) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
            #... do something with the test_result
        except Exception as exc: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(exc))


# In[ ]:





# In[ ]:




