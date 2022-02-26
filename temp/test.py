import sys
import os

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from concurrent import futures
import pandas as pd

class Spoofer(object):
     def __init__(self, user_proxy, country_id=['US'], rand=True, anonym=True,):
          self.user_proxy = user_proxy
          self.country_id = country_id
          self.rand = rand
          self.anonym = anonym
          self.userAgent, self.ip = self.get()
     def get(self):
          ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
          ip = self.user_proxy.split(":")[0]
          # print("Spoofer: ", ip)
          return ua, ip

class DriverOptions(object):
     def __init__(self, user_proxy):
          self.proxy_address = user_proxy.split(":")[0] + ":" + user_proxy.split(":")[1]
          # print("DriverOptions: ", self.proxy_address)
          self.options = Options()
          self.options.add_argument('--no-sandbox')
          self.options.add_argument('--start-maximized')
          self.options.add_argument('--single-process')
          self.options.add_argument('--disable-dev-shm-usage')
          # self.options.add_argument("--incognito")
          self.options.add_argument('--disable-blink-features=AutomationControlled')
          self.options.add_argument('--disable-blink-features=AutomationControlled')
          self.options.add_experimental_option('useAutomationExtension', False)
          self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
          self.options.add_argument("disable-infobars")
          self.helperSpoofer = Spoofer(self.proxy_address)
          self.options.add_argument("user-agent={}".format("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"))
          # self.options.add_argument(f'--proxy-server={self.proxy_address}')
          self.options.add_extension('proxy_auth_plugin.zip')
class WebDriver(DriverOptions,object):
     def __init__(self,user_proxy, path="",):
          DriverOptions.__init__(self,user_proxy)
          self.user_proxy = user_proxy
          print("self.user_proxy", self.user_proxy)
          self.driver_instance = self.get_driver()
     def get_driver(self):
          print("""
          IP:{}
          UserAgent: {}
          """.format(self.helperSpoofer.ip, self.helperSpoofer.userAgent))
          PROXY = {
               "ip":self.user_proxy.split(":")[0],
               "username" : self.user_proxy.split(":")[2],
               "password" : self.user_proxy.split(":")[3],
          }
          print("WebDriver: ", PROXY)
          webdriver.DesiredCapabilities.CHROME['proxy'] = {
               "proxyType":"MANUAL",
               "httpProxy":PROXY['ip'],
               "ftpProxy":PROXY['ip'],
               "sslProxy":PROXY['ip'],
               "noProxy":None,
               'class': "org.openqa.selenium.Proxy",
               "autodetect":False,
               'socksUsername': PROXY['username'],
               'socksPassword': PROXY['password']
          }
          webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
          # self.options.add_extension("./extension_2_0_0_0.crx")
          path = "..\98\chromedriver.exe"
          driver = webdriver.Chrome(path, options=self.options)
          driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
          driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
               "source":
                    "const newProto = navigator.__proto__;"
                    "delete newProto.webdriver;"
                    "navigator.__proto__ = newProto;"
          })
          return driver

def main(user_id):
     user_info = pd.read_csv('../info.csv')
     #몇 개의 계정을 돌릴건지 확인 -> 쓰레드 갯수 때문에 필요함
     user_proxy = str(user_info[user_info['DIR_NUM']==user_id]['PROXY'].values[0])
     print("main: ", user_proxy)
     driver= WebDriver(user_proxy)
     driverinstance = driver.driver_instance
     driverinstance.get("https://www.findip.kr/")
     time.sleep(7)
     driverinstance.get("https://www.naver.com")
     time.sleep(10)
     print("done")

with futures.ThreadPoolExecutor(max_workers=20) as executor: 
     user_info = pd.read_csv('../info.csv')
     user_num = len(user_info)
     print("here", user_info[user_info['DIR_NUM']==2])
     # future_test_results = [ executor.submit(main, i) for i in range(user_num) ] # running same test 6 times, using test number as url
     future_test_results = [ executor.submit(main, 1)] # running same test 6 times, using test number as url
     for future_test_result in future_test_results: 
          try:        
               test_result = future_test_result.result(timeout=None) # can use `timeout` to wait max seconds for each thread               
          except: # can give a exception in some thread, but 
               print('thread generated an exception: {:0}'.format(Exception))