from seleniumwire import webdriver
from time import sleep
import pandas as pd
# 209.61.207.249:64668:run:rKeLShPi

user_info = pd.read_csv('./info.csv')
PROXY = str(user_info[user_info['DIR_NUM']==1]['PROXY'].values[0])
proxy_id = PROXY.split(":")[2]
proxy_pw = PROXY.split(":")[3]
proxy_ip = PROXY.split(":")[0]
proxy_port = PROXY.split(":")[1]
proxy_url = 'http://' + proxy_id + ':' + proxy_pw + "@" + proxy_ip + ":" + proxy_port

options = {
    'proxy': {
        'http': f'{proxy_url}',
        'https':f'{proxy_url}',
        'no_proxy': "localhost,127.0.0.1"
    }
}
# chrome_driver_path = '.\\' + chrome_ver + '\\chromedriver.exe'

# driver =  webdriver.Chrome('.\chromedriver.exe')
driver =  webdriver.Chrome('.\98\chromedriver.exe', seleniumwire_options=options)
driver.get('https://www.nike.com/kr/ko_kr/')
sleep(50)