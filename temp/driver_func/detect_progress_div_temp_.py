from selenium.webdriver.common.by import By 
from time import sleep

def detect_progress_div(Chrome_driver):
    while 1:
        #처리중 div 확인
        try:
            sleep(0.3)
            waiting_div =  Chrome_driver.find_element(By.XPATH, \
                '/html/body/div[position() > 11 and position() < 14]/div[2]')
                # '/html/body/div[22]')
            print("처리 중입니다.")
            if(Chrome_driver.current_url.find("checkout") != -1):
                print("size select success")
                return Chrome_driver, True
            #hidden div check하기
            try:
                if(Chrome_driver.page_source.find("접속자가 많아")!=-1):
                    print("444444444444444444.")
                    return Chrome_driver, False
                    
                # hidden_div_1 = Chrome_driver.find_element(By.XPATH, \
                # '/html/body/div[position()>20 or position()<24]/div[2]')
                # print("111pop up detected.")
                # return Chrome_driver, False
            except:
                print("herer!!!.")
                pass

            
            
        #처리중 div가 안보일 이면 우선 끝
        except:
            print('testtest')
            if(Chrome_driver.current_url.find("checkout") != -1):
                print("size select success")
                return Chrome_driver, True
            elif((Chrome_driver.current_url.find("no-access")!=-1) or (Chrome_driver.current_url.find("singleship")!=-1)):
                print("no-access detected")
                return Chrome_driver, False
            else:
                if(Chrome_driver.current_url.find("checkout") == -1):
                    try:
                        hidden_div_1 = Chrome_driver.find_element(By.XPATH, \
                        # '/html/body/div[position() = 22 or position() = 23]')
                        '/html/body/div[position()>20 or position()<24]/div[2]')
                        print("222pop up detected.")
                        print("hidden_div_1: ", hidden_div_1)
                        print("Chrome_driver.current_url.find(checkout): ", Chrome_driver.current_url)
                        return Chrome_driver, False
                    except:
                        print('hrer!!!222')
                        pass