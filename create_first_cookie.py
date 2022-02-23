from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

import os
import chromedriver_autoinstaller
from time import sleep
import subprocess
import pandas as pd
from concurrent import futures

user_info = pd.read_csv('./info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = len(user_info)

def init(user_num):
    #--------------------------아이디 패스워드 프록시 설정--------------------------
    PROXY = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])

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
    subprocess.Popen(r'{exe} --remote-debugging-port={port_num} --user-data-dir="{cookie}"'.format(exe=chrome_exe_path, cookie=chrome_cookie_path, port_num=proxy_port))
    # subprocess.Popen(r'{exe} --remote-debugging-port={port_num} --user-data-dir="{cookie}"'.format(exe=chrome_exe_path, cookie=chrome_cookie_path, port_num=proxy_port))

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


    #크롬 드라이버 설정
    try:
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    except:
        #크롬 드라이버 버전 관리
        chromedriver_autoinstaller.install(True)  
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    
    driver.get("https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif?hl=en")
# 멀티 쓰레딩
with futures.ThreadPoolExecutor(max_workers=20) as executor: 
                                                                    #user_num을 바꿔서 원하는 쓰레드 개수를 지정할 수 있음)
    future_test_results = [ executor.submit(init, 0) ] # running same test 6 times, using test number as url
    for future_test_result in future_test_results: 
        try:        
            test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
        except: # can give a exception in some thread, but 
            print('thread generated an exception: {:0}'.format(Exception))