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
            #hidden div check하기
            try:
                hidden_div = Chrome_driver.find_element(By.XPATH, \
                '/html/body/div[position() > 21 or position() < 24]')
                print("pop up detected.")
                return Chrome_driver, False
            except:
                pass
            
        #처리중 div가 안보일 이면 우선 끝
        except:
            if(Chrome_driver.current_url.find("checkout") != -1):
                print("size select success")
                return Chrome_driver, True
            else:
                print("no-access detected")
                return Chrome_driver, False