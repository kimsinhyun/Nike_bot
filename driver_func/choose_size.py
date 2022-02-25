from cmath import exp
import time
from tkinter import E
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


from time import sleep
import random




#1. 예약시간에 해당 링크로 이동
#2. 가끔씩 시간이 됐는데도 상품이 안올라왔을 때 최대 10번 동안 새로고침 (너무 많이 하게 되면 벤 먹기 때문에 10번으로 설정함 -> 추후에 변경 가능)
#3. 희망하는 시이즈로 ****한 번만**** 시도 (한 번 실패할 경우 무조건 랜덤으로만 선택 됨)
#4. 희망하는 사이즈가 없을 경우 랜덤으로 사이즈 선택
def goto_page(Chrome_driver, link, size, get_size_mode):
    Chrome_driver.get(link)
    wait = WebDriverWait(Chrome_driver, 10, 0.2)
    # sleep(1)
    #==============================url에 "launch"가 없을 때 (스텔스 구매 페이지)==============================
    if(link.find('launch') == -1):
        #==========================아직 발매가 시작 안됐을 때 계속 새로고침==========================
        for i in range(10): 
            if(Chrome_driver.page_source.find("사이즈 선택") == -1):
                if(Chrome_driver.page_source.find("더 이상 확인 할 수 없는") != -1):
                    Chrome_driver.get(link)
                    sleep(1)
            else:
                break
        #==========================아직 발매가 시작 안됐을 때 계속 새로고침==========================

        action = ActionChains(Chrome_driver)
        #==========================품절일 경우에도 사이즈를 계속 선택해줘야하기 때문에 100번 반복==================
        for i in range(100):
            #======================5번 째 시도마다 한 번씩 새로고침=================
            if((i % 5 == 0) & (i != 0)):
                Chrome_driver.get(link)
            #=======================첫 시도에는 희망하는 사이즈로 시도 (select_size mode)==============================
            item_sold_out = False
            while 1:
                size_elements = Chrome_driver.find_elements(By.XPATH, \
                    '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[*]/div/span[not(@disabled)]')
                if len(size_elements) > 0:
                    break
                else:
                    #활성화 된 사이즈가 없으면 상품이 품절되었는지 확인
                    try:
                        check_item_sold_out = Chrome_driver.find_element(By.XPATH, \
                            "/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[4]/div/div/div[1]/div/span") #품절 되었을 경우 5초마다 계속 확인
                        Chrome_driver.get(link)
                        item_sold_out = True
                        sleep(5)
                        break
                    except:
                        # break
                        continue         
            if(item_sold_out==True):  #상품이 품절된걸 확인하면 다시 사이즈 선택 단계로 돌아가기
                continue


            try:
                print('1111')
                size_element = Chrome_driver.find_element(By.XPATH,\
                    '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[*]/div/span[@typename="' + size + '" and not(contains(@disabled))]')
                print('2222')
            except:
                random_size = random.randint(0,len(size_elements)-1)
                size_element = size_elements[random_size]
            action.move_to_element(size_element).click().perform()
            purchase_btn =  wait.until(EC.presence_of_element_located((By.XPATH,  '//*[@id="btn-buy"]/span')))
            action.move_to_element(purchase_btn).click().perform()


        #===========================구매 페이지로 잘 넘어갔다 확인============================
            
            #======================= 1. no-access로 넘어갔나 확인           =====================
            if(Chrome_driver.current_url.find('checkout') != -1):
                Chrome_driver.get(link)
                continue
            #======================= 1. no-access로 넘어갔나 확인           =====================
            #======================= 2. 처리중이라는 화면이 끝날 때까지 기다림=====================
            temp_check_success = False
            while 1:
                try:
                    waiting_div =  Chrome_driver.find_element(By.XPATH, \
                        '/html/body/div[12]/div[2]')
                except:
                    temp_check_success = True
                    print("break")
                    break
            #======================= 2. 처리중이라는 화면이 끝날 때까지 기다림=====================
            #======================= 3. "접속자가 많아 지연되고 있습니다"일 경우 새로고침 후 재시도====================
            try:
                temp_check_alert = WebDriverWait(Chrome_driver, 0.7, 0.25).until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[22]/div')))
                get_size_mode = "random_size"
                Chrome_driver.get(link)
                continue
            except:
                pass
            #======================= 3. "접속자가 많아 지연되고 있습니다"일 경우 새로고침 후 재시도====================
            #======================= 4. 위에 해당하지 않으면 break ===========================
            if(temp_check_success == True):
                break
            #======================= 4. 위에 해당하지 않으면 break ===========================

        #===========================구매 페이지로 잘 넘어갔다 확인============================
    #==============================url에 "launch"가 없을 때 (스텔스 구매 페이지)==============================





    #==============================url에 "launch"가 있을 때 (스니커즈 구매 페이지) 위와 비슷, 설명 생략==============================
    else:
        #----------------------아직 발매가 시작 안됐을 때--------------------
        for i in range(10): 
            if(Chrome_driver.page_source.find("사이즈 선택") == -1):
                if(Chrome_driver.page_source.find("더 이상 확인 할 수 없는") != -1):
                    Chrome_driver.get(link)
                    sleep(1)
            else:
                break
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
                size_list = wait.until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/a/span')))
                action.move_to_element(size_list).click().perform()
                try:
                    size_element = WebDriverWait(Chrome_driver, 0.5, 0.25).until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/ul/li[@class="list"]/a/span[text()="' + size  + '"]')))
                except:
                    size_elements = Chrome_driver.find_elements(By.XPATH, \
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/ul/li[@class="list"]')
                    random_size = random.randint(0,len(size_elements)-1)
                    size_element = size_elements[random_size]

                action.move_to_element(size_element).click().perform()
                sleep(0.1)

                # #===================구매 버튼 누르기 전에 아무 곳 클릭 (여기서는 상품 이름 명 클릭)===================
                # try:   #막 발매됐을 때랑 이미 전부터 올라와져있는 페이지는 화면 구성이 조금 다르기 때문에 예외처리
                #     temp_element = wait.until(EC.presence_of_element_located((By.XPATH,\
                #         '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[1]/div/h1')))
                # except:
                #     temp_element = wait.until(EC.presence_of_element_located((By.XPATH,\
                #         '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[1]/div[1]/div/h1')))
                # action.move_to_element(temp_element).click().perform()
                # #===================구매 버튼 누르기 전에 아무 곳 클릭 (여기서는 상품 이름 명 클릭)===================
                purchase_btn = WebDriverWait(Chrome_driver, 1, 0.25).until(EC.presence_of_element_located((By.XPATH, \
                        '//*[@id="btn-buy"]/span')))
                action.move_to_element(purchase_btn).click().perform()
            
            #===========================구매 페이지로 잘 넘어갔다 확인============================
            
            # #======================= 1. no-access로 넘어갔나 확인           =====================
            # if(Chrome_driver.current_url.find('checkout') == -1):
            #     Chrome_driver.get(link)
            #     continue
            # #======================= 1. no-access로 넘어갔나 확인           =====================
            #======================= 2. 처리중이라는 화면이 끝날 때까지 기다림(launch 에서는 뺑글뻉글 돌아가는 div)=====================
            temp_check_success = False
            while 1:
                try:
                    waiting_div =  WebDriverWait(Chrome_driver, 1, 0.25).until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[13]/div[1]')))
                except:
                    temp_check_success = True    
                    print("break")
                    break
            #======================= 2. 처리중이라는 화면이 끝날 때까지 기다림=====================
            #======================= 3. "접속자가 많아 지연되고 있습니다"일 경우 새로고침 후 재시도====================
            try:
                print("1")
                comfirm_btn = WebDriverWait(Chrome_driver, 1, 0.25).until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[21]/div/div/div[2]/button')))
                print("2")
                action.move_to_element(comfirm_btn).click().perform()
                continue
            except:
                print("3")
                pass
            #======================= 3. "접속자가 많아 지연되고 있습니다"일 경우 새로고침 후 재시도====================
            #======================= 4. 위에 해당하지 않으면 break ===========================
            if(temp_check_success == True):
                break
            #======================= 4. 위에 해당하지 않으면 break ===========================
    #==============================url에 "launch"가 있을 때 (스니커즈 구매 페이지)#==============================
        