from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


from time import sleep


def choose_address(Chrome_driver): 
    action = ActionChains(Chrome_driver)
    sleep(2)
    wait = WebDriverWait(Chrome_driver, 10,0.25)
    # sleep(1)
    #--------------------------------------여기 부분은 기본 주소 체크 박스 클릭하는 곳---------------------------------
    #--------------------------------------굳이 클릭하지 않아도 잘 동작하기 때문에 시간 절약을 위애 주석처리------------
    #--------------------------------------필요할 경우 주석 해제------------------------------------------------------
    #  default_addr = WebDriverWait(Chrome_driver,3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="shipping_info"]/div[1]/ul/li[3]/div/span/label/i')))
    # while 1:
    #     action.move_to_element(default_addr).click().perform()
    #     sleep(0.2)
    #     if(Chrome_driver.page_source.find("input-checkbox checked") != -1):
    #         break
    #     else:
    #         sleep(1)
    #         if(Chrome_driver.page_source.find("input-checkbox checked") != -1):
    #             break
    #--------------------------------------여기 부분은 기본 주소 체크 박스 클릭하는 곳---------------------------------
    next_stage = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn-next"]')))
    while 1:
        try:
            temp_div = WebDriverWait(Chrome_driver, 2,0.25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="address"]/div[1]/div[1]/dl[1]/dd')))
        except:
            break
    action.move_to_element(next_stage).click().perform()

def choose_payment(Chrome_driver):
    wait = WebDriverWait(Chrome_driver, 6,0.25)
    while 1:
        try:
            action = ActionChains(Chrome_driver)
            #-----------------------------------결제 방식 클릭(아직은 카카오페이만 구현되어 있음(추후에 추가 예정)-------------------------------------------
            payment = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="payment-review"]/div[1]/ul/li[1]/div/div[1]/h6')))
            action.move_to_element(payment).click().perform()

            #------------------------------------구매 동의 체크 박스-----------------------------------
            terms_of_conditions = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="payment-review"]/div[1]/ul/li[2]/form/div/span/label/i')))
            action.move_to_element(terms_of_conditions).click().perform()
            
            #----------------------------------------------결제하기 버튼----------------------------------------------
            complete_purchase = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="complete_checkout"]/button')))
            action.move_to_element(complete_purchase).click().perform()
            break
        except:
            Chrome_driver.refresh()
            sleep(1)
            continue
        
        
