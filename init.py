from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import chromedriver_autoinstaller
from time import sleep
import subprocess
import pandas as pd
from concurrent import futures

from check_login import check_logged_in, login
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

    #각 사용자마다 각각의 쿠키 파일 연결
    chrome_cookie_path = str(os.path.abspath(os.getcwd()))
    chrome_cookie_path = chrome_cookie_path.replace('\개발용dir','')
    chrome_cookie_path = chrome_cookie_path + "\\" +str(user_num) + '\Chrome_cookie'

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    #크롬 실행파일
    chrome_exe_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_driver_path = '.\\' + str(chrome_ver) + '\\chromedriver.exe'

    #proxy config
    proxy_ip = PROXY.split(":")[0]
    proxy_port = PROXY.split(":")[1]
    # proxy_port = "9222"
    proxy_user = PROXY.split(":")[2]
    proxy_pw = PROXY.split(":")[3]
    proxy_address = proxy_ip + ":" + proxy_port

    print(proxy_port)
    proxy = {'address': f'{proxy_address}',
        'username': f'{proxy_user}',
        'password': f'{proxy_pw}'}

    #run chrome by subprocess
    process = subprocess.Popen(f'{chrome_exe_path} --remote-debugging-port={proxy_port} --user-data-dir="{chrome_cookie_path}"')

    capabilities = dict(DesiredCapabilities.CHROME) 
    capabilities['proxy'] = {'proxyType': 'MANUAL',
                            'httpProxy': proxy['address'],
                            'ftpProxy': proxy['address'],
                            'sslProxy': proxy['address'],
                            'noProxy': '',
                            'class': "org.openqa.selenium.Proxy",
                            'autodetect': False,
                            'socksUsername': proxy['username'],
                            'socksPassword': proxy['password']}

    capabilities["pageLoadStrategy"] = "none"

    options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{proxy_port}")
    # options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
    options.add_argument('--profile-directory=Profile 1')

    driver = webdriver.Chrome(executable_path='.\98\chromedriver.exe', desired_capabilities=capabilities, chrome_options=options)


    #크롬 드라이버 설정
    try:
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    except:
        #크롬 드라이버 버전 관리`
        chromedriver_autoinstaller.install(True)  
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    
    # driver.implicitly_wait(2)  
    driver.get("https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=1&acr=1&acq=%EC%95%84%EC%9D%B4%ED%94%BC+%EC%A3%BC%EC%86%8C&qdt=0&ie=utf8&query=%EB%82%B4+%EC%95%84%EC%9D%B4%ED%94%BC+%EC%A3%BC%EC%86%8C+%ED%99%95%EC%9D%B8")
    sleep(2)
    driver.refresh()
    sleep(5)

    driver.get("https://www.nike.com/kr/ko_kr/")
    driver.maximize_window()
    sleep(3)
    sleep(4)
    if(check_logged_in(driver, user_num) == False):
        login(driver, ID, PW, user_num)

    sleep(3)


    #타임 트리거 (예약 실행)
    # if(input_hour != "0" or input_min != "0"):
    #     while True:
    #         if check_time(input_hour, input_min):
    #             print("start")
    #             sleep(0.8)
    #             break

    #job_condition은 총 "사이즈선택", "배송지 선택", "결제방식 선택" 세 가지로 구성됨
    #control flow 용, 각 쓰레드마다 최대 10번씩만 반복
    #여기서는 주로 배송지선택 및 결제방식 선택 시 no-access로 넘어가는 경우를 대비함.
    job_condition = "choose_size"
    for i in range(10):
        if(job_condition=="choose_size"):
            #첫 시도는 희망하는 사이즈로 선택
            if(i == 0):
                get_size_mode = "select_size"
            else:
                get_size_mode = "random_size"
            #first_step -> 사이즈 서택 페이지, 성공하면 choose_address를 return 받아서 다음 스텝으로 넘어간다.
            job_condition = first_step(driver, LINK, SIZE, get_size_mode, job_condition)

        if(job_condition=="choose address"):
            job_condition = second_step(driver,job_condition)

        if(job_condition=="choose_payment"):
            job_condition = thrid_step(driver,user_num, LINK,SIZE,get_size_mode, job_condition)

        if(job_condition == "finish"):
            break

    temp = input("아무 키를 눌러서 종료해주세요 ")
    temp_1 = input("정말 종료 하시겠습니까? (아무 키 입력)")
    process.kill()            
    
def first_step(driver, LINK, SIZE, get_size_mode, job_condition="choose_size"):
    #사이즈 고른 후 주소 선택 화면을 넘어가지 않을 시 5번 시도 (더 많이 하면 no access 뜸)
    for i in range(10):
        goto_page(driver,LINK,SIZE,get_size_mode)
        # 구매버튼 클릭 후 2초 정도 대기
        # sleep(2)
        #사이즈 선택 및 구매버튼 클릭 완료 후(여기 부분의 예외처리는 goto_page 안에 구현되어 있음)
        #배송지 선택 창으로 넘어가는지 확인
        #no-access 혹은 사이즈 선택 창에서 성공적으로 실행되지 않았다면 random_size 모드로 사이즈 선택 총 5번 실행
        if(driver.current_url.find('checkout') == -1):
            get_size_mode = 'random_size'
        else:
            job_condition = 'choose address'
            return job_condition

def second_step(driver,job_condition="choose address"):
    for i in range(10):
        choose_address(driver)
        # sleep(2)
        #배송지 선택 화면으로 넘어온 후 payment선택 화면으로 정상적으로 이동하지 못했을 시
        #1. no-access이면 job_condition을 사이즈 선택으로 다시 돌아가게
        #2. 다른 오류로 payment 창으로 넘어가지 못했을 경우 새로고침 후 다시 배송지 선택
        #3. payment로 성공적으로 넘어가면 다음 스탭 시도
        if(driver.current_url.find('checkout') == -1):
            #no-access가 뜨는 경우 사이즈 선택으로 다시 돌아가게 choose_size를 return
            if(driver.current_url.find('no-access') != -1):
                job_condition = 'choose_size'
                return job_condition
        else:
            #만약 문제 없이 결제수단 선택 페이지로 잘 들어가졌다면
            try:
                payment = WebDriverWait(driver, 5,0.25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="payment-review"]/div[1]/ul/li[1]/div/div[1]/h6/img')))
                return 'choose_payment'
            except:
                driver.refresh()
                continue
            # if(driver.page_source.find('실시간계좌이체') != 1):
            #     job_condition = 'choose_payment'
            #     return job_condition
            # #혹시 모를 팝업창이 뜨거나하면 새로고침 후 재시도
            # else:
            #     driver.refresh()
            #     sleep(1)
            #     continue

def thrid_step(driver,user_num, LINK,SIZE,get_size_mode, job_condition="choose_payment", ):
    for i in range(10):
        try:
            print("start third step")
            choose_payment(driver)
        except:
            print('here??')
            return "choose_size"
        sleep(2)
        
        #만약 no-access로 넘어가게 되면 다시 size 선택
        if(driver.current_url.find('no-access') != -1):
            return "choose_size"
        else:
            # 1. 주문 생성 오류 감지 시
            if(driver.page_source.find("생성 오류") != -1):
                print("생성 오류")
                driver.refresh()
                sleep(2)
                continue

            try:
                qr_code = WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[17]')))
                print(user_num, "th 아이디 성공!")
                return "finish"
            except:
                print("여기")
                return "finish"

            
            # ------지금 이부분이 제대로 동작이 안되서 우선 뺏음 있으면 더 좋은데 없어도 잘 될 듯--------
            # 2-1. 만약 QR코드가 제대로 떴을 경우
            # sleep(10) 
            # if(driver.page_source.find("스캔하면") != -1):
            #     print(user_num, "th user success!")
            #     return "finish"
            # # 2-2. 만약 제대로 뜨지 않았을 경우
            # else:
            #     print('here')
            #     return "finish"


# 멀티 쓰레딩
with futures.ThreadPoolExecutor(max_workers=20) as executor: 
                                                                    #user_num을 바꿔서 원하는 쓰레드 개수를 지정할 수 있음)
    future_test_results = [ executor.submit(init, i) for i in range(user_num) ] # running same test 6 times, using test number as url
    # future_test_results = [ executor.submit(init, i) for i in range(2) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))