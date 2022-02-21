from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

proxy = {'address': '209.61.207.249:64668',
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
options.add_extension("./extension_2_0_0_0.crx")
driver = webdriver.Chrome(executable_path='.\98\chromedriver.exe', desired_capabilities=capabilities, chrome_options=options)

driver.get("chrome-extension://ggmdpepbjljkkkdaklfihhngmmgmpggp/options.html")

driver.find_element_by_id("login").send_keys("run")
driver.find_element_by_id("password").send_keys("rKeLShPi")
driver.find_element_by_id("retry").clear()
driver.find_element_by_id("retry").send_keys("2")


driver.find_element_by_id("save").click()
driver.get("https://www.nike.com/kr/ko_kr/")
# 209.61.207.249:64668:run:rKeLShPi