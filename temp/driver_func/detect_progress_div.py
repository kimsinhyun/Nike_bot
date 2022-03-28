from selenium.webdriver.common.by import By 
from time import sleep

def detect_progress_div(Chrome_driver):
    while 1:
        #처리중 div 확인
        if(Chrome_driver.current_url.find("checkout")!=-1):
            return Chrome_driver, True
        elif((Chrome_driver.current_url.find("no-access")!=-1) or (Chrome_driver.current_url.find("singleship")!=-1)):
            print("no-access detected")
            return Chrome_driver, False
        elif(Chrome_driver.page_source.find("접속자가 많아")!=-1):
            print("popup_1 detected")
            return Chrome_driver, False
        elif(Chrome_driver.page_source.find("재고가")!=-1):
            print("popup_2 detected")
            return Chrome_driver, False
