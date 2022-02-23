
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException

from time import sleep
import pyperclip

def check_logged_in(Chrome_driver, user_num):
    wait = WebDriverWait(Chrome_driver, 10, 0.5)
    try:
        login_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div/div[1]/div/div/ul/li[3]/a')))
        return False
    except TimeoutException:
        print(str(user_num) + '번 째 아이디는 이미 로그인 되어 있습니다')
        return True

#1. 클립보드를 사용하는 방식이기 때문에 csv에 적어놨던 로그인 정보대로가 아닌 여러 창들이 한 아이디로 로그인 될 확률이 높음
#2. 할 수는 있는데 완벽하게 할려면 로그인 시간을 좀 오래두고 해야할 수 있음
#3. 지금은 당장 급한게 아니니까 로그인 정도는 수동으로 한 번만 해놓으면 앞으로 실행할 때마다 쿠키 파일이 설정되어 있어서 알아서 로그인 되어 있기 떄문에 문제 없음 (추후에 수정 요청 시 추가 삽가능합니다!)
def login(Chrome_driver,user_ID,user_PW, user_num):
    wait = WebDriverWait(Chrome_driver, 10,0.5)
    sleep(int(user_num) * 11)
    print(str(user_num) + '번 째 아이디의 로그인을 시작합니다')
    try:
        action = ActionChains(Chrome_driver)
        login_btn = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div/div[1]/div/div/ul/li[3]/a')))
#         login_btn = driver.find_element(By.XPATH,'/html/body/header/div/div[1]/div/div/ul/li[3]/a')
        action.move_to_element(login_btn).click().perform()
    except TimeoutException:
        print(str(user_num) + '번 째 아이디는 이미 로그인 되어 있습니다')
        return
    
    pyperclip.copy(user_ID)
    ID_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_username"]')))
    for i in range(30):
        sleep(0.01)
        ID_input.send_keys(Keys.BACKSPACE)
    ID_input.send_keys(Keys.CONTROL + 'v')

    pyperclip.copy(user_PW)
    PW_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_password"]')))
    for i in range(30):
        sleep(0.01)
        PW_input.send_keys(Keys.BACKSPACE)
    PW_input.send_keys(Keys.CONTROL + 'v')


    action = ActionChains(Chrome_driver)
    submit_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="common-modal"]/div/div/div/div[2]/div/div[2]/div/button')))
    #무작위로 딜레이 주기
    action.move_to_element(submit_btn).click().perform()