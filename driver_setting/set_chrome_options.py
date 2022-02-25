from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium import webdriver

def get_chrome_options(proxy,proxy_port):
    #chrome driver option
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
    capabilities["pageLoadStrategy"] = "none"
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("debuggerAddress", f"127.0.0.1:{proxy_port}")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
    options.add_argument('--profile-directory=Profile 1')

    return capabilities, options