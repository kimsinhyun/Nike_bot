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
    sleep(1)
    #==============================url에 "launch"가 없을 때 (스텔스 구매 페이지)==============================
    if(link.find('launch') == -1):
        #==========================아직 발매가 시작 안됐을 때 계속 새로고침==========================
        for i in range(10): 
            if(Chrome_driver.page_source.find("사이즈 선택") == -1):
                Chrome_driver.get(link)
                sleep(1)
        #==========================아직 발매가 시작 안됐을 때 계속 새로고침==========================

        action = ActionChains(Chrome_driver)
        #==========================사이즈를 계속 선택해줘야하기 때문에 100번 반복==================
        for i in range(100):
            #======================5번 째 시도마다 한 번씩 새로고침=================
            if((i % 5 == 0) & (i != 0)):
                Chrome_driver.get(link)
                sleep(1)
            # sleep(1.5)
            #=======================첫 시도에는 희망하는 사이즈로 시도 (select_size mode)==============================
            if(get_size_mode == "select_size"):
                size_element = WebDriverWait(Chrome_driver, 1).until(EC.element_to_be_clickable((By.XPATH,\
                    '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[1]/div/span[*]/label[text()=' + size  + ']')))
                # sleep(1)
                action.move_to_element(size_element).click().perform()

                sleep(0.1)
                purchase_btn =  WebDriverWait(Chrome_driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-buy"]/span')))
                action.move_to_element(purchase_btn).click().perform()
                sleep(0.2)
            #=======================첫 시도에는 희망하는 사이즈로 시도 (select_size mode)==============================

            #=======================이후 계속 랜덤 사이즈로 (select_size mode)==============================
            elif(get_size_mode == "random_size"):
                size_elements = Chrome_driver.find_elements(By.XPATH, \
                    '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[1]/div/span[not(@disabled="disabled")]')
                random_size = random.randint(0,len(size_elements))
                sleep(0.1)
                size_element = size_elements[random_size]
                action.move_to_element(size_element).click().perform()
                purchase_btn =  WebDriverWait(Chrome_driver, 1).until(EC.element_to_be_clickable((By.XPATH,  '//*[@id="btn-buy"]/span')))
                action.move_to_element(purchase_btn).click().perform()
                sleep(0.2)
            #=======================이후 계속 랜덤 사이즈로 (select_size mode)==============================


            #======================= A. 만약 "사이즈를 선택해주세요" 라는 문구가 안뜨면 성공한 것으로 간주 ====================
            #======================= B. 사이즈를 선택 했는데 주소 선택 페이지로 안가고 "재고 없음"이란 팝업창이 뜨거나 ======== 
            #======================= 다른 이유 때문에 성공적으로 가지 못하는 경우 해당 예외처리는 부모에서 처리 됨 ============
            if(Chrome_driver.page_source.find("사이즈를 선택해 주세요") == -1):
                break
            #======================= 한 번만이라도 희망하는 사이즈로 구매를 실패할 경우 쭉 random size로 ================
            else:
                get_size_mode="random_size"
    #==============================url에 "launch"가 없을 때 (스텔스 구매 페이지)==============================





    #==============================url에 "launch"가 있을 때 (스니커즈 구매 페이지) 위와 비슷, 설명 생략==============================
    else:
        #----------------------아직 발매가 시작 안됐을 때--------------------
        for i in range(10): 
            if(Chrome_driver.page_source.find("사이즈 선택") == -1): 
                Chrome_driver.get(link)
                sleep(2)
        #----------------------아직 발매가 시작 안됐을 때--------------------
        action = ActionChains(Chrome_driver)
        for i in range(100):
            if((i % 3 == 0) & (i != 0)):
                Chrome_driver.get(link)
                sleep(2)
            # sleep(1.5)
            if(get_size_mode == "select_size"):
                size_list = WebDriverWait(Chrome_driver, 1).until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/a/span')))
                action.move_to_element(size_list).click().perform()
                
                sleep(0.5)
                size_element = WebDriverWait(Chrome_driver, 1).until(EC.presence_of_element_located((By.XPATH,\
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/ul/li[*]/a/span[text()=' + size  + ']')))
                
                try:
                    action.move_to_element(size_element).click().perform()
                except:
                    action.move_to_element(size_list).click().perform()
                    sleep(0.3)
                    action.move_to_element(size_element).click().perform()

                #===================구매 버튼 누르기 전에 아무 곳 클릭 (여기서는 상품 이름 명 클릭)===================
                # sleep(0.5)
                try:   #막 발매됐을 때랑 이미 전부터 올라와져있는 페이지는 화면 구성이 조금 다르기 때문에 예외처리
                    temp_element = WebDriverWait(Chrome_driver, 1).until(EC.presence_of_element_located((By.XPATH,\
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[1]/div/h1')))
                except:
                    temp_element = WebDriverWait(Chrome_driver, 1).until(EC.presence_of_element_located((By.XPATH,\
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[1]/div[1]/div/h1')))
                action.move_to_element(temp_element).click().perform()
                #===================구매 버튼 누르기 전에 아무 곳 클릭 (여기서는 상품 이름 명 클릭)===================
                
                sleep(0.2)
                purchase_btn =  WebDriverWait(Chrome_driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-buy"]/span')))
                action.move_to_element(purchase_btn).click().perform()
            
            #random으로 구매할 수 있는 사이즈를 선택
            elif(get_size_mode == "random_size"):
                size_list = WebDriverWait(Chrome_driver, 1).until(EC.presence_of_element_located((By.XPATH, \
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/a/span')))
                action.move_to_element(size_list).click().perform()

                sleep(0.5)
                size_elements = Chrome_driver.find_elements(By.XPATH, \
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/ul/li[@class="list"]')
                random_size = random.randint(0,len(size_elements)-1)
                print("(launch)random_size: ", random_size)
                size_element = size_elements[random_size]
                try:
                    action.move_to_element(size_element).click().perform()
                except:
                    action.move_to_element(size_list).click().perform()
                    sleep(0.5)
                    action.move_to_element(size_element).click().perform()

                #===================구매 버튼 누르기 전에 아무 곳 클릭 (여기서는 상품 이름 명 클릭)===================
                # sleep(0.5)
                try:   #막 발매됐을 때랑 이미 전부터 올라와져있는 페이지는 화면 구성이 조금 다르기 때문에 예외처리
                    temp_element = WebDriverWait(Chrome_driver, 1).until(EC.presence_of_element_located((By.XPATH,\
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[1]/div/h1')))
                except:
                    temp_element = WebDriverWait(Chrome_driver, 1).until(EC.presence_of_element_located((By.XPATH,\
                        '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[1]/div[1]/div/h1')))
                action.move_to_element(temp_element).click().perform()
                #===================구매 버튼 누르기 전에 아무 곳 클릭 (여기서는 상품 이름 명 클릭)===================

                sleep(0.2)
                purchase_btn = WebDriverWait(Chrome_driver, 1).until(EC.element_to_be_clickable((By.XPATH,  '//*[@id="btn-buy"]/span')))
                action.move_to_element(purchase_btn).click().perform()
            
            if(Chrome_driver.page_source.find("사이즈를 선택해 주세요") == -1):
                break
            else:
                get_size_mode = "random_size"
    #==============================url에 "launch"가 있을 때 (스니커즈 구매 페이지)#==============================
        