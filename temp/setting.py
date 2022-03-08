import os
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

if  getattr(sys, 'frozen', False): 
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    driver = webdriver.Chrome(chromedriver_path)
else:
    driver = webdriver.Chrome()


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
          return ua, ip

class DriverOptions(object):
     def __init__(self, user_proxy,user_num):
        # cookie_dir = "..\\cookies\\" +str(user_num) + '\\Chrome_cookie\\Default'
     #    C:\Users\Administrator\Desktop\sinhyun code\nike\dist\cookies\4\Chrome_cookie
     #    C:\Users\Administrator\Desktop\sinhyun code\nike\temp\dist\cookies\4\Chrome_cookie
        cookie_dir = str(os.path.abspath(os.getcwd())) + "\\cookies\\" +str(user_num) + '\Chrome_cookie'
        print("cookie_dir: " + cookie_dir)
        self.proxy_address = user_proxy.split(":")[0] + ":" + user_proxy.split(":")[1]
        self.options = Options()
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.options.add_argument(f"--user-data-dir={cookie_dir}") 
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
        self.options.add_extension('proxy_config/' + str(user_num) + 'th_proxy_auth_plugin.zip')
class WebDriver(DriverOptions,object):
     def __init__(self,user_proxy,user_num, path="",):
          DriverOptions.__init__(self,user_proxy,user_num)
          self.user_proxy = user_proxy
          self.driver_instance = self.get_driver()
     def get_driver(self):
          # print("""
          # IP:{}
          # UserAgent: {}
          # """.format(self.helperSpoofer.ip, self.helperSpoofer.userAgent))
          PROXY = {
               "ip":self.user_proxy.split(":")[0],
               "username" : self.user_proxy.split(":")[2],
               "password" : self.user_proxy.split(":")[3],
          }
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
          path = ".\chromedriver.exe"
          driver = webdriver.Chrome(path, options=self.options)
          driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
          driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
               "source":
                    "const newProto = navigator.__proto__;"
                    "delete newProto.webdriver;"
                    "navigator.__proto__ = newProto;"
          })
          return driver



# def save_cookie(driver,user_num):
#     save_path = '../cookies/' + user_num + "/Chrome_cookie"
#     with open(save_path, 'wb') as filehandler:
#         pickle.dump(driver.get_cookies(), filehandler)
# def load_cookie(driver,user_num):
#     load_path = '../cookies/' + user_num + "/Chrome_cookie"
#     with open(load_path, 'rb') as cookiesfile:
#         cookies = pickle.load(cookiesfile)
#         for cookie in cookies:
#             print(cookie)
#             driver.add_cookie(cookie)