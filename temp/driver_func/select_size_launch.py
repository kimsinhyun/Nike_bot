from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from time import sleep
import random

def select_size_launch(Chrome_driver, size_select_box, size_elements, size):
    wait = WebDriverWait(Chrome_driver, 10, 0.1)
    action = ActionChains(Chrome_driver)
    #사용자가 희망 size를 입력했었다면 
    if(size != "nan"):    
        try:
            print('select size mode')
            size_element = Chrome_driver.find_element(By.XPATH, \
                    '/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]/ul/li[@class="list"]/a/span[text()=' + size  + ']')
        #혹시 사용자가 입력을 잘 못 했거나 sold out이면 랜덤 사이즈 선택
        except:
            print('sold out or input error, choose random size')
            random_size = random.randint(0,len(size_elements)-1)
            size_element = size_elements[random_size]

    #사용자가 size를 비워뒀다면 랜덤 사이즈 선택
    else:
        print('user not entered size, choose random size')
        random_size = random.randint(0,len(size_elements)-1)
        size_element = size_elements[random_size]
    size_element.click()
    sleep(0.5)

    #너무 빨라서 사이즈 클릭이 잘 안됐을 경우 선택 될 때까지 클릭
    check_size_selected = Chrome_driver.find_element(By.XPATH,\
        "/html/body/div[1]/div/div[1]/div[2]/div[1]/section/div[2]/aside/div[2]/div/div/div/div/form/div/div[1]")
    while(check_size_selected.get_attribute("class") != "select-box width-max pc rendered"):
        size_select_box.click()
        sleep(0.5)
        size_element.click()
        sleep(0.5)
    purchase_btn = WebDriverWait(Chrome_driver, 10, 0.25).until(EC.presence_of_element_located((By.XPATH, \
        '//*[@id="btn-buy"]/span')))
    purchase_btn.click()

    return Chrome_driver