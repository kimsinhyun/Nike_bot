
from selenium.webdriver.common.by import By 

from time import sleep

def wait_size_elements_ko_kr(Chrome_driver,link):
    while 1:
        print("waitting for size list")
        size_elements = Chrome_driver.find_elements(By.XPATH, \
            '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[*]/div/span[not(@disabled)]')
        #사이즈 리스트가 로딩 됐으면 elements 리턴 후 사이즈 선택 문구
        if len(size_elements) > 0:
            print("start choose size")
            return Chrome_driver, size_elements
        #사이즈 리스트가 0일 때 no-accses나 singleship이면 새로고침 
        elif((Chrome_driver.current_url.find("no-access")!=-1) or (Chrome_driver.current_url.find("singleship")!=-1)):
            print("no-access detected, goto size page again")
            Chrome_driver.get(link)  
            continue
        #사이즈 리스트가 0일 때 no-access랑 singleship 모두 아닐 경우
        else:
            #품절 되었다면
            try:
                __check_item_sold_out = Chrome_driver.find_element(By.XPATH, \
                    "/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[4]/div/div/div[1]/div/span") #품절 되었을 경우 5초마다 계속 확인
                Chrome_driver.get(link)  
                print("품절되었습니다")
                sleep(5)
                continue
            #아직 selectable 하지 않는 상태
            except:
                continue         