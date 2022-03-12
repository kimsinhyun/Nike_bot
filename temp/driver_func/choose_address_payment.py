from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from time import sleep

def choose_address(Chrome_driver): 
    action = ActionChains(Chrome_driver)
    # wait = WebDriverWait(Chrome_driver, 1,0.25)
    while 1:
        try:
            print("checking choose_address temp_div")
            temp_div = Chrome_driver.find_element(By.XPATH, '//*[@id="address"]/div[1]/div[1]/dl[1]/dd')
            break
        except:
            #===================no-access 한 번 더 확인===================
            if(Chrome_driver.current_url.find("no-access") != -1):
                print("choose address (no-access)")
                Chrome_driver.refresh()
                sleep(1)
            else:
                print("temp_div loading...")
            continue
    while 1:
        try:
            next_stage = Chrome_driver.find_element(By.XPATH, '//*[@id="btn-next"]')
            print("address next_stage")
            action.move_to_element(next_stage).click().perform()
            break
        except:
            print("address test")
            continue


def choose_payment(Chrome_driver):
    wait = WebDriverWait(Chrome_driver, 6,0.25)
    while 1:
        print("choose_payment")
        try:
            action = ActionChains(Chrome_driver)
            #-----------------------------------결제 방식 클릭(아직은 카카오페이만 구현되어 있음(추후에 추가 예정)-------------------------------------------
            payment = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="payment-review"]/div[1]/ul/li[1]/div/div[1]/h6')))
            action.move_to_element(payment).click().perform()
            #-----------------------------------만약 클릭이 너무 빨라서 클릭이 안됐으면 다시 클릭--------------------------
            while 1:
                try:
                    print("payment test")
                    check_payment_clicked = WebDriverWait(Chrome_driver, 0.5,0.1).until(EC.presence_of_element_located((By.XPATH, \
                        '//*[@id="payment-review"]/div[1]/ul/li[1]/div/div[1]')))
                    if(check_payment_clicked.get_attribute("class") == "payment-method-item active"):
                        break
                    else:
                        action.move_to_element(payment).click().perform()
                except:
                    action.move_to_element(payment).click().perform()
                    break
            #-----------------------------------만약 클릭이 너무 빨라서 클릭이 안됐으면 다시 클릭--------------------------

            #------------------------------------구매 동의 체크 박스-----------------------------------
            terms_of_conditions = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="payment-review"]/div[1]/ul/li[2]/form/div/span/label/i')))
            sleep(0.1)
            action.move_to_element(terms_of_conditions).click().perform()
            
            #----------------------------------------------결제하기 버튼----------------------------------------------
            complete_purchase = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="complete_checkout"]/button')))
            sleep(0.1)
            action.move_to_element(complete_purchase).click().perform()
            break
        except:
            print("re choose payment")
            Chrome_driver.refresh()
            sleep(1)
            continue