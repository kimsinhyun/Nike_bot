from seleniumwire import webdriver
from time import sleep
import pandas as pd

user_info = pd.read_csv('./info.csv')
PROXY = str(user_info[user_info['DIR_NUM']==1]['PROXY'].values[0])
proxy_id = PROXY.split(":")[2]
proxy_pw = PROXY.split(":")[3]
proxy_ip = PROXY.split(":")[0]
proxy_port = PROXY.split(":")[1]
print(proxy_id)
print(proxy_pw)
print(proxy_ip)
print(proxy_port)
proxy_url = 'http://' + proxy_id + ':' + proxy_pw + "@" + proxy_ip + ":" + proxy_port
print(proxy_url)

options = {
    'proxy': {
        'http': f'{proxy_url}',
        'https':f'{proxy_url}',
        'no_proxy': "localhost,127.0.0.1"
    }
}
driver =  webdriver.Chrome('.\98\chromedriver.exe', seleniumwire_options=options)
driver.get('https://www.google.co.kr/')
sleep(50)