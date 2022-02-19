from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains



import os
import chromedriver_autoinstaller
from time import sleep
import subprocess
import pandas as pd
from concurrent import futures

from check_login import check_logged_in
from check_time import check_time
from choose_address_payment import choose_address, choose_payment
from choose_size import goto_page


user_info = pd.read_csv('./info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)

input_hour = input("set hour: ")
input_min = input("set min: ")

def init(user_num):
    #--------------------------아이디 패스워드 프록시 설정--------------------------
    ID = str(user_info[user_info['DIR_NUM']==user_num]['ID'].values[0])
    PW = str(user_info[user_info['DIR_NUM']==user_num]['PW'].values[0])
    PROXY = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])
    LINK = str(user_info[user_info['DIR_NUM']==user_num]['LINK'].values[0])
    SIZE = str(user_info[user_info['DIR_NUM']==user_num]['SIZE'].values[0])
    #--------------------------아이디 패스워드 프록시 설정--------------------------

    #------------크롬 버전 확인 및 각 사용자별 exe파일 경로 및 쿠키 경로------------
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    chrome_exe_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
#     chrome_exe_path = str(os.path.abspath(os.getcwd()))
#     chrome_exe_path = chrome_exe_path.replace('\개발용dir','')
#     chrome_exe_path = chrome_exe_path + "\\" +str(user_num)  + '\Chrome\Application\chrome.exe'

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
#     #------------------------자동 제어모드 우회------------------------------
    
    
#     #---------------------------프록시 서버 설정------------------------------
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
    
    driver.implicitly_wait(3)  
    driver.get("https://www.nike.com/kr/ko_kr/")
    
    try:
        driver.maximize_window()
    except:
        pass
    
    sleep(4)
    check_logged_in(driver,ID, PW, user_num)
    sleep(5)
    

    if(input_hour != "0" or input_min != "0"):
        # 로그인 되고 나서 타임 트리거 걸어 줌
            while True:
                if check_time(input_hour, input_min):
                    print("start")
                    sleep(0.8)
                    break


    #임시
#     sleep(1)
#     #임시

    job_condition = "choose_size"
    for i in range(5):
        if(job_condition=="choose_size"):
            print("111")
            get_size_mode = "select_size"
            job_condition = first_step(driver, LINK, SIZE, get_size_mode, job_condition)

        if(job_condition=="choose address"):
            print("222")
            job_condition = second_step(driver,job_condition)

        if(job_condition=="choose_payment"):
            print("333")
            choose_payment(driver)
            #주문 생성 오류 감지
            sleep(3)
            #1. 오류 없이 결제 창이 잘 떴을 경우
            if(driver.page_source.find("오류가") == -1):
                break
            else:
                action = ActionChains(driver)
                submit_btn =  WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[17]/div/div/div[2]/button')))
                action.move_to_element(submit_btn).click().perform()
                
    
def first_step(driver, LINK, SIZE, get_size_mode, job_condition="choose_size"):
    #사이즈 고른 후 주소 선택 화면을 넘어가지 않을 시 5번 시도 (더 많이 하면 no access 뜸)
    for i in range(5):
        goto_page(driver,LINK,SIZE,get_size_mode)
        sleep(2)
        #사이즈 선택 및 구매버튼 클릭 완료 후(여기 부분의 예외처리는 goto_page 안에 구현되어 있음)
        #배송지 선택 창으로 넘어가는지 확인
        #no-access 혹은 사이즈 선택 창에서 성공적으로 실행되지 않았다면 random_size 모드로 사이즈 선택 총 5번 실행
        if(driver.current_url.find('checkout') == -1):
            get_size_mode = 'random_size'
        else:
            job_condition = 'choose address'
            return job_condition

def second_step(driver,job_condition="choose address"):
    for i in range(5):
        choose_address(driver)
        sleep(2)
        #배송지 선택 화면으로 넘어온 후 payment선택 화면으로 정상적으로 이동하지 못했을 시
        #1. no-access이면 job_condition을 사이즈 선택으로 다시 돌아가게
        #2. 다른 오류로 payment 창으로 넘어가지 못했을 경우 새로고침 후 다시 배송지 선택
        #3. payment로 성공적으로 넘어가면 다음 스탭 시도
        print("here")
        if(driver.current_url.find('checkout') == -1):
            if(driver.current_url.find('error/no-access') != -1):
                job_condition = 'choose_size'
                return job_condition
            else:
                continue
        else:
            # if(driver.page_source.find('실시간계좌이체') != 1):
            job_condition = 'choose_payment'
            return job_condition







with futures.ThreadPoolExecutor(max_workers=20) as executor: 
    future_test_results = [ executor.submit(init, i) for i in range(5) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
            #... do something with the test_result
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))