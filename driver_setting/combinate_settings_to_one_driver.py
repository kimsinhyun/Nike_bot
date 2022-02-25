import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


from driver_setting.user_info import get_user_info
import subprocess
from driver_setting.chrome_cookie_driver_exe import get_cookie_driver_exe
from driver_setting.set_chrome_options import get_chrome_options
from selenium import webdriver
import chromedriver_autoinstaller

def execute_subprocess_and_return_driver(user_info, user_num):
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
    capabilities, options = get_chrome_options(proxy_dict,proxy_port)
    #크롬 버전 관리 예외처리
    try:
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    except:
        #크롬 드라이버 버전 관리
        chromedriver_autoinstaller.install(True)  
        driver = webdriver.Chrome(executable_path=f'{chrome_driver_path}',desired_capabilities=capabilities, options=options)
    return driver