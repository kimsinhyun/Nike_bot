from selenium.webdriver.common.by import By 

def check_size_select_success(Chrome_driver):
    #check-out 페이지로 잘 들어왔을 경우
    if(Chrome_driver.current_url.find("checkout") != -1):
        print("size select success")
        return Chrome_driver, True
    #성공적으로 들어가지 못 했을 경우: no-access 체크 
    elif(Chrome_driver.current_url.find("no-access") == -1):
        print("no-access detected when selecting size, choose size again")
        return Chrome_driver, False
    #성공적으로 들어가지 못 했을 경우: 팝업 체크
    else:
        try:
            popup_div = Chrome_driver.find_element(By.XPATH, \
                '/html/body/div[position() > 21 and position() < 24]')
            print("popup detected, choose size again")
        except:
            pass
        return Chrome_driver, False

