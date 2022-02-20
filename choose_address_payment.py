from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


from time import sleep


def choose_address(Chrome_driver):
    action = ActionChains(Chrome_driver)
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
    next_stage = WebDriverWait(Chrome_driver,3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-next"]')))
    action.move_to_element(next_stage).click().perform()

def choose_payment(Chrome_driver):
    while 1:
        try:
            action = ActionChains(Chrome_driver)
            sleep(0.7)
            #-----------------------------------결제 방식 클릭(아직은 카카오페이만 구현되어 있음(추후에 추가 예정)-------------------------------------------
            payment = WebDriverWait(Chrome_driver,2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="payment-review"]/div[1]/ul/li[1]/div/div[1]/h6/img')))
            action.move_to_element(payment).click().perform()
            sleep(0.05)

            #------------------------------------구매 동의 체크 박스-----------------------------------
            terms_of_conditions = WebDriverWait(Chrome_driver,2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="payment-review"]/div[1]/ul/li[2]/form/div/span/label/i')))
            action.move_to_element(terms_of_conditions).click().perform()
            
            #----------------------------------------------결제하기 버튼----------------------------------------------
            sleep(1.5)
            complete_purchase = WebDriverWait(Chrome_driver,2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="complete_checkout"]/button')))
            action.move_to_element(complete_purchase).click().perform()
            break
        except:
            Chrome_driver.refresh()
            sleep(1)
            continue
        
        
