import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver_func.choose_size import goto_page
from driver_func.choose_address_payment import choose_address, choose_payment


def first_step(driver, LINK, SIZE, get_size_mode, retry_time, job_condition="choose_size"):
    #사이즈 고른 후 주소 선택 화면을 넘어가지 않을 시 5번 시도 (더 많이 하면 no access 뜸)
    for i in range(30):
        driver = goto_page(driver,LINK,SIZE,get_size_mode, retry_time)
        
        #사이즈 선택 및 구매버튼 클릭 완료 후(여기 부분의 예외처리는 goto_page 안에 구현되어 있음)
        #배송지 선택 창으로 넘어가는지 확인
        #no-access 혹은 사이즈 선택 창에서 성공적으로 실행되지 않았다면 random_size 모드로 사이즈 선택 총 5번 실행
        if(driver.current_url.find('checkout') == -1):
            get_size_mode = 'choose_size'
            print("choose size -> choose address (no-access)")
        else:
            job_condition = 'choose address'
            return job_condition

def second_step(driver,job_condition="choose address"):
    for i in range(30):
        choose_address(driver)
        #배송지 선택 화면으로 넘어온 후 payment선택 화면으로 정상적으로 이동하지 못했을 시
        #1. no-access이면 job_condition을 사이즈 선택으로 다시 돌아가게
        #2. 다른 오류로 payment 창으로 넘어가지 못했을 경우 새로고침 후 다시 배송지 선택
        #3. payment로 성공적으로 넘어가면 다음 스탭 시도
        if(driver.current_url.find("singleship") != -1):
            print("singleship")
            job_condition = 'choose_size'
            return job_condition
        elif(driver.current_url.find('checkout') == -1):
            #no-access가 뜨는 경우 사이즈 선택으로 다시 돌아가게 choose_size를 return
            if(driver.current_url.find('no-access') != -1):
                print("choose_address -> payment (no-access)")
                job_condition = 'choose_size'
                return job_condition
        else:
            #만약 문제 없이 결제수단 선택 페이지로 잘 들어가졌다면
            try:
                payment = WebDriverWait(driver, 2,0.25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="payment-review"]/div[1]/ul/li[1]/div/div[1]/h6/img')))
                return 'choose_payment'
            except:
                driver.refresh()
                continue

def thrid_step(driver,user_num, LINK,SIZE,get_size_mode, job_condition="choose_payment", ):
    print("start third step")
    for i in range(30):
        try:
            choose_payment(driver)
        except:
            print('here??')
            return "choose_size"
        sleep(2)
        
        #만약 no-access로 넘어가게 되면 다시 size 선택
        if(driver.current_url.find('no-access') != -1):
            return "choose_size"
        else:
            # 1. 주문 생성 오류 감지 시
            if(driver.page_source.find("선택한 상품의 재고가 없습니다") != -1):
                print("선택한 상품의 재고가 없습니다")
                return "choose_size"
            try:
                # qr_code = WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[17]')))
                qr_code = driver.find_element(By.XPATH, '/html/body/div[17]')
                print(user_num, "th 아이디 성공!")
                return "finish"
            except:
                print("여기")
                return "finish"