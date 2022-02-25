from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chromedriver_autoinstaller
from time import sleep
import subprocess
import pandas as pd
from concurrent import futures

from driver_func.check_login import check_logged_in, login
from driver_func.check_time import check_time
from driver_func.choose_address_payment import choose_address, choose_payment
from driver_func.choose_size import goto_page

from driver_setting.user_info import get_user_info
from driver_setting.chrome_cookie_driver_exe import get_cookie_driver_exe
from driver_setting.set_chrome_options import get_chrome_options
from driver_setting.combinate_settings_to_one_driver import execute_subprocess_and_return_driver
from driver_func.show_proxy_ip import show_proxy_ip
from driver_func.time_trigger import time_trigger

user_info = pd.read_csv('./info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)

input_hour = input("set hour: ")
input_min = input("set min: ")

def init(user_num):
    #유저 정보
    ID, PW, PROXY, LINK, SIZE,proxy_dict =  get_user_info(user_info, user_num)

    # 드라이버 설정
    driver = execute_subprocess_and_return_driver(user_info,user_num)

    #프록시 적용 확인용 (주석처리 해도 상관 없음)
    show_proxy_ip(driver=driver, hold_time=10)

    #나이키 코리아로 이동
    driver.get("https://www.nike.com/kr/ko_kr/")
    driver.maximize_window()
    
    
    #로그인 확인 (아직 자동로그인은 너무 벤을 자주 먹어서 제외함)
    sleep(3)
    check_logged_in(driver, user_num)
    # temp = input("로그인을 모두 마쳤습니다")
    # if(check_logged_in(driver, user_num) == False):
    #     login(driver, ID, PW, user_num)



    #타임 트리거 (예약 실행)
    time_trigger(input_hour, input_min)

    #job_condition은 총 "사이즈선택", "배송지 선택", "결제방식 선택" 세 가지로 구성됨
    #control flow 용, 각 쓰레드마다 최대 10번씩만 반복
    #여기서는 주로 배송지선택 및 결제방식 선택 시 no-access로 넘어가는 경우를 대비함.
    job_condition = "choose_size"
    for i in range(10):
        if(job_condition=="choose_size"):
            #첫 시도는 희망하는 사이즈로 선택
            get_size_mode = "select_size"
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


# 멀티 쓰레딩
with futures.ThreadPoolExecutor(max_workers=20) as executor: 
                                                                    #user_num을 바꿔서 원하는 쓰레드 개수를 지정할 수 있음)
    future_test_results = [ executor.submit(init, i) for i in range(user_num) ] # running same test 6 times, using test number as url
    # future_test_results = [ executor.submit(init, 1) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))