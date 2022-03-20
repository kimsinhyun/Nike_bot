from asyncio import wait_for
from pymysql import NULL
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
        for i in range(30):
            print("checking item uploaded")
            if(Chrome_driver.page_source.find("사이즈 선택") != -1):
                break
            else:
                if(Chrome_driver.page_source.find("더 이상 확인 할 수 없는") != -1):
                    Chrome_driver.get(link)
                    # sleep(1)
            
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
                print("waitting for size list")
                size_elements = Chrome_driver.find_elements(By.XPATH, \
                    '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[*]/div/span[not(@disabled)]')
                if len(size_elements) > 0:
                    break
                else:
                    temp=1
                    print("품절되었습니다")
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

            # print("size is :", size)
            # print("type of size is :", type(size))
            if(size != "nan"):    
                try:
                    print('selecte size mode')
                    size_element = Chrome_driver.find_element(By.XPATH,\
                        # '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[*]/div/span[@typename="' + size + '" and not(contains(@disabled))]')
                        '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[*]/div/span[*]/label[text()=' + size  + ']')
                    # print(size_element.get_attribute("class"))
                    if(size_element.get_attribute("class") == "sd-out"):
                        print('choose random size 1')
                        random_size = random.randint(0,len(size_elements)-1)
                        size_element = size_elements[random_size]    
                except:
                    print('choose random size 2')
                    random_size = random.randint(0,len(size_elements)-1)
                    size_element = size_elements[random_size]
            else:
                print('size empty, choose random size')
                random_size = random.randint(0,len(size_elements)-1)
                size_element = size_elements[random_size]
            action.move_to_element(size_element).click().perform()
            #너무 빨라서 사이즈 클릭이 잘 안됐을 경우 다시 한 번 더 클릭
            if(size_element.get_attribute("class") != "selected"):
                action.move_to_element(size_element).click().perform()
            purchase_btn =  wait.until(EC.presence_of_element_located((By.XPATH,  '//*[@id="btn-buy"]/span')))
            action.move_to_element(purchase_btn).click().perform()

        #===========================구매 페이지로 잘 넘어갔다 확인 ============================
            #======================= 1. no-access로 넘어갔나 확인 ============================
            if(Chrome_driver.current_url.find('no-access') != -1):
                # Chrome_driver.get(link)
                continue
            #======================= 1. no-access로 넘어갔나 확인 ============================
            #======================= 2. 처리중이라는 화면이 끝날 때까지 기다림 =====================
            temp_check_success = False
            while 1:
                try:
                    waiting_div =  Chrome_driver.find_element(By.XPATH, \
                        '/html/body/div[*]/div[2]')
                    if(Chrome_driver.current_url.find("checkout") != -1):
                        temp_check_success = True
                        break
                    elif(Chrome_driver.page_source.find("지연되고 있습니다")!=-1):
                        break
                except:
                    temp_check_success = True
                    print("break")
                    break
            #======================= 2. 처리중이라는 화면이 끝날 때까지 기다림 =====================
            #======================= 3. "접속자가 많아 지연되고 있습니다"일 경우 새로고침 후 재시도====================
            try:
                print("temp_check_alert")
                temp_check_alert = WebDriverWait(Chrome_driver, 0.5, 0.25).until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[*]/div')))
                if(Chrome_driver.current_url.find("checkout") != -1):
                    break
                get_size_mode = "select_size"
                # Chrome_driver.get(link)
                continue
            except:
                pass
            #======================= 3. "접속자가 많아 지연되고 있습니다"일 경우 새로고침 후 재시도====================

            #======================= 4. 한 번 더 no-access 체크 ============================
            # if(Chrome_driver.current_url.find('no-access') != -1):
            #     print("bbb")
            #     continue
            #======================= 4. 한 번 더 no-access 체크 ============================

            print("temp_check_success", temp_check_success)

            #======================= 4. 위에 해당하지 않으면 break ===========================
            if(temp_check_success == True):
                break
            #======================= 4. 위에 해당하지 않으면 break ===========================

        #===========================구매 페이지로 잘 넘어갔다 확인============================
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
        