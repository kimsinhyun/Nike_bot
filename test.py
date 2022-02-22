from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
import subprocess
import chromedriver_autoinstaller
import os
from check_login import check_logged_in, login
import pandas as pd
from time import sleep
from choose_size import goto_page

#기본 설정
user_info = pd.read_csv('./info.csv')
#몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
user_num = 1


#--------------------------아이디 패스워드 프록시 설정--------------------------
ID = str(user_info[user_info['DIR_NUM']==user_num]['ID'].values[0])
PW = str(user_info[user_info['DIR_NUM']==user_num]['PW'].values[0])
PROXY = str(user_info[user_info['DIR_NUM']==user_num]['PROXY'].values[0])
LINK = str(user_info[user_info['DIR_NUM']==user_num]['LINK'].values[0])
SIZE = str(user_info[user_info['DIR_NUM']==user_num]['SIZE'].values[0])

chrome_cookie_path = str(os.path.abspath(os.getcwd()))
chrome_cookie_path = chrome_cookie_path.replace('\개발용dir','')
chrome_cookie_path = chrome_cookie_path + "\\" +str(user_num) + '\Chrome_cookie'
#기본 설정

chrome_exe_path = "0\Chrome\Application\chrome_proxy.exe"
chrome_driver_path = '.\\' + "98" + '\\chromedriver.exe'
subprocess.Popen(r'{exe} --remote-debugging-port={port_num} --user-data-dir="{cookie}"'.format(exe=chrome_exe_path, cookie=chrome_cookie_path, port_num=str(58758)))

proxy = {'address': '209.61.207.133:58758',
     'username': 'run',
     'password': 'rKeLShPi'}

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
options.add_argument("--start-maximized")
options.add_experimental_option("debuggerAddress", f"209.61.207.133:58758")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
# options.add_experimental_option("useAutomationExtension", False)
# options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_argument(f'--user-data-dir={chrome_cookie_path}')
options.add_extension("./extension_2_0_0_0.crx")

driver = webdriver.Chrome(executable_path='.\98\chromedriver.exe', desired_capabilities=capabilities, chrome_options=options)

driver.get("chrome-extension://ggmdpepbjljkkkdaklfihhngmmgmpggp/options.html")

driver.find_element_by_id("login").send_keys("run")
driver.find_element_by_id("password").send_keys("rKeLShPi")
driver.find_element_by_id("retry").clear()
driver.find_element_by_id("retry").send_keys("2")


driver.find_element_by_id("save").click()
sleep(3)
driver.get("https://www.nike.com/kr/ko_kr/")

# if(check_logged_in(driver, user_num) == False):
#         login(driver, ID, PW, user_num)

sleep(5)
# goto_page(driver, LINK, SIZE, 'select_size')
sleep(50)
# def goto_page(Chrome_driver, link, size, get_size_mode):

# 209.61.207.133:58758:run:rKeLShPi