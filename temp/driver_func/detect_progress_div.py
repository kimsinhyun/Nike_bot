from selenium.webdriver.common.by import By 
from time import sleep

def detect_progress_div(Chrome_driver):
    while 1:
        #처리중 div 확인
        try:
            sleep(0.3)
            waiting_div =  Chrome_driver.find_element(By.XPATH, \
                '/html/body/div[position() > 11 and position() < 14]/div[2]')
            print("처리 중입니다.")
            if(Chrome_driver.current_url.find("checkout") != -1):
                return Chrome_driver
        #처리중 div가 안보일 이면 우선 끝
        except:
            return Chrome_driver