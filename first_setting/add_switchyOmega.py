from selenium import webdriver
import subprocess
import chromedriver_autoinstaller
from concurrent import futures
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
import pandas as pd
from time import sleep
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from driver_setting.user_info import get_user_info
from driver_setting.chrome_cookie_driver_exe import get_cookie_driver_exe
from driver_setting.set_chrome_options import get_chrome_options

user_info = pd.read_csv('../info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)

def add_switchOmega(user_num):
    #기본 설정
    #--------------------------아이디 패스워드 프록시 설정--------------------------
    ID, PW, PROXY, LINK, SIZE,proxy_dict =  get_user_info(user_info, user_num)
    proxy_port = proxy_dict['proxy_port']

    #크롬 버전
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    #쿠키, 드라이버 ,exe
    chrome_cookie_path, chrome_exe_path, chrome_driver_path = get_cookie_driver_exe(chrome_ver, user_num)
    
    #run chrome by subprocess
    process = subprocess.Popen(f'{chrome_exe_path} --remote-debugging-port={proxy_port} --user-data-dir="{chrome_cookie_path}"')

    #driver option
    capabilities, options = get_chrome_options(proxy_dict,proxy_dict['proxy_port'])

    #크롬 버전 관리 예외처리
    try:
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    except:
        #크롬 드라이버 버전 관리
        chromedriver_autoinstaller.install(True)  
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)

    driver.get('chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/1')
    driver.maximize_window()

    protocal_select =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div/section[1]/div/table/tbody[1]/tr[1]/td[2]/select')))
    

    sleep(1)
    protocal_select.click()
    sleep(1)

    protocal =  WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[2]/div/section[1]/div/table/tbody[1]/tr[1]/td[2]/select/option[2]')))
    protocal.click()
    sleep(1)

    profile1_proxy_ip =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,   '/html/body/div[1]/main/div[2]/div/section[1]/div/table/tbody[1]/tr[1]/td[3]/input')))
    profile1_proxy_ip.click()
    profile1_proxy_ip.clear()
    profile1_proxy_ip.send_keys(proxy_dict['proxy_ip'])
    sleep(1)
    profile1_proxy_port =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div/section[1]/div/table/tbody[1]/tr[1]/td[4]/input')))
    profile1_proxy_port.clear()
    profile1_proxy_port.send_keys(proxy_dict['proxy_port'])
    sleep(1)
    profile_id_pw_ptn =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,   '/html/body/div[1]/main/div[2]/div/section[1]/div/table/tbody[1]/tr[1]/td[5]/button/span')))
    profile_id_pw_ptn.click()
    sleep(1)

    profile_id =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/form/div[2]/div[2]/div/div/input')))
    profile_id.clear()
    profile_id.send_keys(proxy_dict['username'])
    sleep(1)
    profile_pw =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/form/div[2]/div[3]/div/input[1]')))
    profile_pw.clear()
    profile_pw.send_keys(proxy_dict['password'])
    sleep(1)
    submit_proxy_btn =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/form/div[3]/button[2]')))
    submit_proxy_btn.click()
    sleep(1)

    try:
        apply_change_btn=  WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/nav/li[13]/a')))
    except:
        apply_change_btn=  WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/nav/li[11]/a')))
        
    apply_change_btn.click()
    sleep(1)

    interface_btn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/nav/li[2]/a')))
    interface_btn.click()
    sleep(1)
    startup_profile =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/section[3]/div[1]/div/div/button')))
    startup_profile.click()
    sleep(1)
    default_profile =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/section[3]/div[1]/div/div/ul/li[2]/a')))
    default_profile.click()
    sleep(1)

    try:
        apply_change_btn=  WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/nav/li[13]/a')))
    except:
        apply_change_btn=  WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/nav/li[11]/a')))
    apply_change_btn.click()

    sleep(1)
    driver.get('https://www.google.com/search?q=what+is+my+ip&oq=what+is+my+ip&aqs=chrome..69i57j0i20i263i512j0i512l7.847j0j9&sourceid=chrome&ie=UTF-8')
    sleep(2)
    driver.refresh()
    temp = input("enter any key to terminate: ")
    # process.kill()
with futures.ThreadPoolExecutor(max_workers=20) as executor: 
                                                                    #user_num을 바꿔서 원하는 쓰레드 개수를 지정할 수 있음)
    # future_test_results = [ executor.submit(add_switchOmega, i) for i in range(2) ] # running same test 6 times, using test number as url
    future_test_results = [ executor.submit(add_switchOmega, i) for i in range(user_num) ] # running same test 6 times, using test number as url
    # future_test_results = [ executor.submit(add_switchOmega, 0) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))