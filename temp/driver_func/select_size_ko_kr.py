from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from time import sleep
import random

def select_size_ko_kr(Chrome_driver, size_elements, size):
    wait = WebDriverWait(Chrome_driver, 10, 0.1)
    action = ActionChains(Chrome_driver)
    #사용자가 희망 size를 입력했었다면 
    if(size != "nan"):    
        try:
            print('selecte size mode')
            size_element = Chrome_driver.find_element(By.XPATH,\
                # '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[*]/div/span[@typename="' + size + '" and not(contains(@disabled))]')
                '/html/body/section/section/section/article/article[2]/div/div[4]/div/div[2]/form/div[2]/div[2]/div[*]/div/span[*]/label[text()=' + size  + ']')
            if(size_element.get_attribute("class") == "sd-out"):
                print('choose random size 1')
                random_size = random.randint(0,len(size_elements)-1)
                size_element = size_elements[random_size]    
        #혹시 사용자가 입력을 잘 못 했을 때 랜덤 사이즈 선택
        except:
            print('size entered incorrectly')
            random_size = random.randint(0,len(size_elements)-1)
            size_element = size_elements[random_size]

    #사용자가 size를 비워뒀다면 
    else:
        print('user not entered size, choose random size')
        random_size = random.randint(0,len(size_elements)-1)
        size_element = size_elements[random_size]
    # action.move_to_element(size_element).click().perform()
    size_element.click()
    sleep(0.1)
    #너무 빨라서 사이즈 클릭이 잘 안됐을 경우 다시 한 번 더 클릭
    if(size_element.get_attribute("class") != "selected"):
        # action.move_to_element(size_element).click().perform()
        size_element.click()
        sleep(0.1)
    purchase_btn =  wait.until(EC.presence_of_element_located((By.XPATH,  '//*[@id="btn-buy"]/span')))
    # action.move_to_element(purchase_btn).click().perform()
    purchase_btn.click()

    return Chrome_driver