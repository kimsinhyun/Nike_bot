from selenium.webdriver.common.keys import Keys
from copyreg import add_extension
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
import subprocess
import chromedriver_autoinstaller
from concurrent import futures
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver import ActionChains
import os
import pandas as pd
from time import sleep

user_info = pd.read_csv('./info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)

def add_switchOmega(user_num):
    #기본 설정
    #--------------------------아이디 패스워드 프록시 설정--------------------------
    ID = str(user_info[user_info['DIR_NUM']==user_num]['ID'].values[0])
    PW = str(user_info[user_info['DIR_NUM']==user_num]['PW'].values[0])
    PROXY = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])
    LINK = str(user_info[user_info['DIR_NUM']==user_num]['LINK'].values[0])
    SIZE = str(user_info[user_info['DIR_NUM']==user_num]['SIZE'].values[0])

    #각 사용자마다 각각의 쿠키 파일 연결
    chrome_cookie_path = str(os.path.abspath(os.getcwd()))
    chrome_cookie_path = chrome_cookie_path.replace('\개발용dir','')
    chrome_cookie_path = chrome_cookie_path + "\\" +str(user_num) + '\Chrome_cookie'

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    #크롬 실행파일
    chrome_exe_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_driver_path = '.\\' + str(chrome_ver) + '\\chromedriver.exe'

    #proxy config
    proxy_ip = PROXY.split(":")[0]
    proxy_port = PROXY.split(":")[1]
    # proxy_port = "9222"
    proxy_user = PROXY.split(":")[2]
    proxy_pw = PROXY.split(":")[3]
    proxy_address = proxy_ip + ":" + proxy_port

    print(proxy_port)
    proxy = {'address': f'{proxy_address}',
        'username': f'{proxy_user}',
        'password': f'{proxy_pw}'}

    #run chrome by subprocess
    subprocess.Popen(f'{chrome_exe_path} --remote-debugging-port={proxy_port} --user-data-dir="{chrome_cookie_path}"')

    capabilities = dict(DesiredCapabilities.CHROME)
    capabilities['proxy'] = {'proxyType': 'MANUAL',
                            'httpProxy': proxy['address'],
                            'ftpProxy': proxy['address'],
                            'sslProxy': proxy['address'],
                            'noProxy': '',
                            'class': "org.openqa.selenium.Proxy",
                            'autodetect': False,
                            'socksUsername': proxy['username'],
                            'socksPassword': proxy['password']}

    options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{proxy_port}")
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
    options.add_argument('--profile-directory=Profile 1')

    driver = webdriver.Chrome(executable_path='.\98\chromedriver.exe', desired_capabilities=capabilities, chrome_options=options)



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
    profile1_proxy_ip.send_keys(proxy_ip)
    sleep(1)
    profile1_proxy_port =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div/section[1]/div/table/tbody[1]/tr[1]/td[4]/input')))
    profile1_proxy_port.clear()
    profile1_proxy_port.send_keys(proxy_port)
    sleep(1)
    profile_id_pw_ptn =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,   '/html/body/div[1]/main/div[2]/div/section[1]/div/table/tbody[1]/tr[1]/td[5]/button/span')))
    profile_id_pw_ptn.click()
    sleep(1)

    profile_id =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/form/div[2]/div[2]/div/div/input')))
    profile_id.clear()
    profile_id.send_keys(proxy_user)
    sleep(1)
    profile_pw =  WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/form/div[2]/div[3]/div/input[1]')))
    profile_pw.clear()
    profile_pw.send_keys(proxy_pw)
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

with futures.ThreadPoolExecutor(max_workers=20) as executor: 
                                                                    #user_num을 바꿔서 원하는 쓰레드 개수를 지정할 수 있음)
    future_test_results = [ executor.submit(add_switchOmega, i) for i in range(2) ] # running same test 6 times, using test number as url
    # future_test_results = [ executor.submit(add_switchOmega, i) for i in range(user_num) ] # running same test 6 times, using test number as url
    # future_test_results = [ executor.submit(add_switchOmega, 0) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))