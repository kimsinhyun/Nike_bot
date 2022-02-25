import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By 
from time import sleep
import pyperclip
from concurrent import futures

from driver_setting.user_info import get_user_info
from driver_setting.combinate_settings_to_one_driver import execute_subprocess_and_return_driver
from driver_func.show_proxy_ip import show_proxy_ip


user_info = pd.read_csv('../info.csv')
user_num = len(user_info)

#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
def fisrt_login(user_num):
    #유저 정보
    ID, PW, _, _, _,_ = get_user_info(user_info, user_num)
    # 드라이버 설정
    driver = execute_subprocess_and_return_driver(user_info,user_num)
    #프록시 적용 확인용 (주석처리 해도 상관 없음)
    show_proxy_ip(driver=driver, hold_time=10)
    #나이키 코리아로 이동
    driver.get("https://www.nike.com/kr/ko_kr/")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10,1)
    sleep(int(user_num) * 11)
    print(str(user_num) + '번 째 아이디의 로그인을 시작합니다')
    try:
        action = ActionChains(driver)
        login_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div/div[1]/div/div/ul/li[3]/a')))
#         login_btn = driver.find_element(By.XPATH,'/html/body/header/div/div[1]/div/div/ul/li[3]/a')
        action.move_to_element(login_btn).click().perform()
    except TimeoutException:
        print(str(user_num) + '번 째 아이디는 이미 로그인 되어 있습니다')
        return
    
    pyperclip.copy(ID)
    ID_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_username"]')))
    sleep(1)
    ID_input.send_keys(Keys.CONTROL + 'v')

    pyperclip.copy(PW)
    PW_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_password"]')))
    sleep(1)
    PW_input.send_keys(Keys.CONTROL + 'v')


    action = ActionChains(driver)
    submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="common-modal"]/div/div/div/div[2]/div/div[2]/div/button')))
    action.move_to_element(submit_btn).click().perform()


with futures.ThreadPoolExecutor(max_workers=20) as executor: 
                                                                    #user_num을 바꿔서 원하는 쓰레드 개수를 지정할 수 있음)
    future_test_results = [ executor.submit(fisrt_login, i) for i in range(user_num) ] # running same test 6 times, using test number as url
    # future_test_results = [ executor.submit(init, 1) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))