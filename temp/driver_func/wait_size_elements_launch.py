from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep

def wait_size_elements_launch(Chrome_driver,link, retry_time):
    #Buy 버튼 활성화 전까지 대기
    while 1:
        purchase_btn = Chrome_driver.find_elements(By.XPATH, \
            '//*[@id="btn-buy"]/span')
        #구매버튼이 0보다 크다면, 즉 활성화 됐다면
        if(len(purchase_btn) > 0):
            print("size loaded")
            size_select_box = Chrome_driver.find_element(By.XPATH, \
                "/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/a") #품절 되었을 경우 5초마다 계속 확인
            size_select_box.click()
            size_elements = Chrome_driver.find_elements(By.XPATH, \
                "/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/ul/li[@class='list']")
            return Chrome_driver, size_select_box, size_elements
        elif((Chrome_driver.current_url.find("no-access")!=-1) or (Chrome_driver.current_url.find("singleship")!=-1)):
            print("no-access detected, goto size page again")
            Chrome_driver.get(link)  
            continue
        else:
            try:
                __check_item_sold_out = Chrome_driver.find_element(By.XPATH, \
                "/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/div[1]") #품절 되었을 경우 5초마다 계속 확인
                Chrome_driver.get(link)  
                print("품절되었습니다")
                sleep(retry_time)
                continue
            except:
                #품절된 것도 아니라면 계속 구매버튼 탐색
                continue

    