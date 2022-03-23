from asyncio import wait_for
from pymysql import NULL
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from select_size_ko_kr import select_size_ko_kr
from wait_size_elements_ko_kr import wait_size_elements_ko_kr
from checking_item_uploaded import checking_item_uploaded
from detect_progress_div import detect_progress_div
from check_size_select_success import check_size_select_success

from time import sleep
import random

#1. 예약시간에 해당 링크로 이동
#2. 가끔씩 시간이 됐는데도 상품이 안올라왔을 때 최대 10번 동안 새로고침 (너무 많이 하게 되면 벤 먹기 때문에 10번으로 설정함 -> 추후에 변경 가능)
#3. 희망하는 시이즈로 ****한 번만**** 시도 (한 번 실패할 경우 무조건 랜덤으로만 선택 됨)
#4. 희망하는 사이즈가 없을 경우 랜덤으로 사이즈 선택
def goto_page(Chrome_driver, link, size, get_size_mode):
    Chrome_driver.get(link)
    wait = WebDriverWait(Chrome_driver, 10, 0.1)
    # sleep(1)
    #==============================url에 "launch"가 없을 때 (스텔스 구매 페이지)==============================
    if(link.find('launch') == -1):
        #==========================아직 발매가 시작 안됐을 때 계속 새로고침==========================
        Chrome_driver = checking_item_uploaded(Chrome_driver, link)

        #==========================최대 100번 재시도==================
        for i in range(100):
            #======================5번 째 시도마다 한 번씩 새로고침=================
            if((i % 5 == 0) & (i != 0)):
                Chrome_driver.get(link)

            #=======================사이즈 element 들이 활성화 될 때까지 대기==============================
            Chrome_driver, size_elements = wait_size_elements_ko_kr(Chrome_driver, link)

            #======================= 사이즈 선택 ============================
            Chrome_driver = select_size_ko_kr(Chrome_driver, size_elements, size)

            #===========================우선 처리 중이라는 div가 끝날 때까지 기다림============================
            Chrome_driver = detect_progress_div(Chrome_driver)

            #===========================no-access로 갔는지 혹은 "지연 되고 있습니다" or "재고가 없습니다" 일 경우 다시 사이즈 선택으로 재시도============================
            Chrome_driver, size_select_success = check_size_select_success(Chrome_driver)

            if(size_select_success == False):
                Chrome_driver.get(link)
                continue
            else:
                return

    #==============================url에 "launch"가 없을 때 (스텔스 구매 페이지)==============================





    #==============================url에 "launch"가 있을 때 (스니커즈 구매 페이지) 위와 비슷, 설명 생략==============================
    else:
        #----------------------아직 발매가 시작 안됐을 때--------------------
        for i in range(30): 
            if(Chrome_driver.page_source.find("사이즈 선택") != -1):
                print("item uploaded")
                break
            else:
                if(Chrome_driver.page_source.find("Coming Soon") != -1):
                    print("Coming soon")
                    Chrome_driver.get(link)
                    sleep(1)
        #----------------------아직 발매가 시작 안됐을 때--------------------
        action = ActionChains(Chrome_driver)
        for i in range(20):
            if((i % 3 == 0) & (i != 0)):
                Chrome_driver.get(link)
                # sleep(2)
            # sleep(1.5)
            #============= Buy 버튼이 생길 때까지 기다리기==================
            while 1:
                try:
                    purchase_btn = Chrome_driver.find_element(By.XPATH, \
                        '//*[@id="btn-buy"]/span')
                    break
                except:
                    continue
            #============= Buy 버튼이 생길 때까지 기다리기==================
            if(get_size_mode == "select_size"):
                # size_list = wait.until(EC.presence_of_element_located((By.XPATH, \
                #         '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/a/span')))
                size_list = Chrome_driver.find_element(By.XPATH, \
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/a/span')
                action.move_to_element(size_list).click().perform()
                try:
                    size_element = Chrome_driver.find_element(By.XPATH, \
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/ul/li[@class="list"]/a/span[text()=' + size  + ']')
                except:
                    size_elements = Chrome_driver.find_elements(By.XPATH, \
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/ul/li[@class="list"]')
                    random_size = random.randint(0,len(size_elements)-1)
                    size_element = size_elements[random_size]

                action.move_to_element(size_element).click().perform()
                sleep(0.05)

                purchase_btn = WebDriverWait(Chrome_driver, 1, 0.25).until(EC.presence_of_element_located((By.XPATH, \
                        '//*[@id="btn-buy"]/span')))
                action.move_to_element(purchase_btn).click().perform()
            
            #===========================구매 페이지로 잘 넘어갔다 확인============================
            
            # #======================= 1. no-access로 넘어갔나 확인           =====================
            if(Chrome_driver.current_url.find('no-access') != -1):
                Chrome_driver.get(link)
                continue
            # #======================= 1. no-access로 넘어갔나 확인           =====================
            #======================= 2. 처리중이라는 화면이 끝날 때까지 기다림(launch 에서는 뺑글뻉글 돌아가는 div)=====================
            temp_check_success = False
            while 1:
                try:
                    waiting_div =  WebDriverWait(Chrome_driver, 1, 0.25).until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[*]/div[1]')))
                    if(Chrome_driver.current_url.find("checkout") != -1):
                        temp_check_success = True
                        break
                except:
                    temp_check_success = True    
                    print("break")
                    break
            #======================= 2. 처리중이라는 화면이 끝날 때까지 기다림 =====================
            #======================= 3. "접속자가 많아 지연되고 있습니다"일 경우 새로고침 후 재시도 ====================
            try:
                print("1")
                comfirm_btn = WebDriverWait(Chrome_driver, 0.5, 0.25).until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[*]/div/div/div[2]/button')))
                if(Chrome_driver.current_url.find("checkout") != -1):
                    break
                print("2")
                # action.move_to_element(comfirm_btn).click().perform()
                continue
            except:
                if(Chrome_driver.current_url.find("checkout") != -1):
                    break
                print("3")
                pass
            #======================= 3. "접속자가 많아 지연되고 있습니다"일 경우 새로고침 후 재시도====================
            #======================= 4. 위에 해당하지 않으면 break ===========================
            if(temp_check_success == True):
                break
            #======================= 4. 위에 해당하지 않으면 break ===========================
    #==============================url에 "launch"가 있을 때 (스니커즈 구매 페이지)#==============================
        